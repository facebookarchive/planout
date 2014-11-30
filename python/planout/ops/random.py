import hashlib
from .base import PlanOutOpSimple


class PlanOutOpRandom(PlanOutOpSimple):
    LONG_SCALE = float(0xFFFFFFFFFFFFFFF)

    def getUnit(self, appended_unit=None):
        unit = self.getArgMixed('unit')
        if type(unit) is not list:
            unit = [unit]
        if appended_unit is not None:
            unit += [appended_unit]
        return unit

    def getHash(self, appended_unit=None):
        if 'full_salt' in self.args:
            full_salt = self.getArgString('full_salt')  # do typechecking
        else:
            salt = self.getArgString('salt')
            full_salt = '%s.%s' % (self.mapper.experiment_salt, salt)
        unit_str = '.'.join(map(str, self.getUnit(appended_unit)))
        hash_str = '%s.%s' % (full_salt, unit_str)
        return int(hashlib.sha1(hash_str).hexdigest()[:15], 16)

    def getUniform(self, min_val=0.0, max_val=1.0, appended_unit=None):
        zero_to_one = self.getHash(appended_unit) / PlanOutOpRandom.LONG_SCALE
        return min_val + (max_val - min_val) * zero_to_one


class RandomFloat(PlanOutOpRandom):

    def simpleExecute(self):
        min_val = self.getArgFloat('min')
        max_val = self.getArgFloat('max')

        return self.getUniform(min_val, max_val)


class RandomInteger(PlanOutOpRandom):

    def simpleExecute(self):
        min_val = self.getArgInt('min')
        max_val = self.getArgInt('max')

        return min_val + self.getHash() % (max_val - min_val + 1)


class BernoulliTrial(PlanOutOpRandom):

    def simpleExecute(self):
        p = self.getArgNumeric('p')
        assert p >= 0 and p <= 1.0, \
            '%s: p must be a number between 0.0 and 1.0, not %s!' \
            % (self.__class__, p)

        rand_val = self.getUniform(0.0, 1.0)
        return 1 if rand_val <= p else 0


class BernoulliFilter(PlanOutOpRandom):

    def simpleExecute(self):
        p = self.getArgNumeric('p')
        values = self.getArgList('choices')
        assert p >= 0 and p <= 1.0, \
            '%s: p must be a number between 0.0 and 1.0, not %s!' \
            % (self.__class__, p)

        if len(values) == 0:
            return []
        return [i for i in values if self.getUniform(0.0, 1.0, i) <= p]


class UniformChoice(PlanOutOpRandom):

    def simpleExecute(self):
        choices = self.getArgList('choices')

        if len(choices) == 0:
            return []
        rand_index = self.getHash() % len(choices)
        return choices[rand_index]


class WeightedChoice(PlanOutOpRandom):

    def simpleExecute(self):
        choices = self.getArgList('choices')
        weights = self.getArgList('weights')

        if len(choices) == 0:
            return []
        cum_weights = dict(enumerate(weights))
        cum_sum = 0.0
        for index in cum_weights:
            cum_sum += cum_weights[index]
            cum_weights[index] = cum_sum
        stop_value = self.getUniform(0.0, cum_sum)
        for index in cum_weights:
            if stop_value <= cum_weights[index]:
                return choices[index]


class Sample(PlanOutOpRandom):

    # implements Fisher-Yates shuffle
    def simpleExecute(self):
        # copy the list of choices so that we don't mutate it
        choices = [x for x in self.getArgList('choices')]
        if 'draws' in self.args:
            num_draws = self.getArgInt('draws')
            assert num_draws <= len(choices), \
                "%s: cannot make %s draws when only %s choices are available" \
                % (self.__class__, num_draws, len(choices))
        else:
            num_draws = len(choices)

        for i in xrange(len(choices) - 1, 0, -1):
            j = self.getHash(i) % (i + 1)
            choices[i], choices[j] = choices[j], choices[i]
        return choices[:num_draws]
