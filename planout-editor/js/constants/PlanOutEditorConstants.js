/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * PlanOutEditorConstants
 */

var keyMirror = require('react/lib/keyMirror');

module.exports = {

  ActionTypes: keyMirror({
    /**
     * Constants for actions
     *
     */

    // Creating and destroying PlanOutTesterBoxes
    CREATE_TESTER: null,
    LOAD_SERIALIZED_TESTERS: null,
    INIT_TESTER_PANEL: null,
    TESTER_DESTROY: null,

    // Updating PlanOutTesterBox states
    TESTER_USER_UPDATE_TEST: null,
    TESTER_SERVER_UPDATE_TEST: null,
    TESTER_INVALID_TEST_FORM: null,
    TESTER_REFRESH_TEST: null,
    TESTER_REFRESH_ALL_TESTS: null,

    // Code Editor / compilation related actions
    EDITOR_LOAD_SCRIPT: null,
    EDITOR_COMPILE_SCRIPT: null,
    EDITOR_UPDATE_COMPILED_CODE: null
  }),

  TesterStatusCodes: keyMirror({
    SUCCESS: null,
    FAILURE: null,
    INVALID_FORM: null,
    PENDING: null
  }),

  TesterBoxTypes: keyMirror({
    TEST: null,
    PLAYGROUND: null
  })
};
