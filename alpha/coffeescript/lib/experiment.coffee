class Experiment

  constructor: ->
    @inputs = arguments # might not be what i want
    @exposure_logged = false
    @_salt = undefined
    @in_experiment = true
    #?
    @name = self.class.name
    @auto_exposure_log = true

    @setup  # sets name, salt, etc.

    @assignment = new Assignment(salt)
    @assigned = false

    @logger = undefined
    @setup

  _assign: ->
    @configure_logger()
    @assign(@assignment, @inputs)
    @in_experiment = @assignment.get("", @in_experiment)
    @assigned = true

  setup: ->
    return

  salt: ->
    @_salt or @name

  configure_logger: ->
    undefined

  requires_assignment: ->
    @_assign() if !@assigned

  is_logged: ->
    @logged

  requires_exposure_logging: ->
    @log_exposure() if @auto_exposure_log and @in_experiment and !@exposure_logged

  get_params: ->
    @requires_assignment()
    @requires_exposure_logging()
    @assignment.get_params()

  get: (name, default) ->
    @requires_assignment()
    @requires_exposure_logging()
    @assignment.get(name, default)

  assign: ->
    return

  log_event: (event_type, extras) ->
    if extras?
      extra_payload =
        event: event_type
        extra_data: extras.clone #clone
    else
      extra_payload =
        event: event_type

    @log(@as_blob(extra_payload))

  log_exposure: (extras) ->
    @exposure_logged = true
    @log_event("exposure", extras)

  as_blob: (extras = {}) ->
    d = {
      name: @name
      time: new Date().getTime()
      salt: salt #salt
      inputs: @inputs
      params: @assignment.data
    }

    d.merge!(extras) #??
