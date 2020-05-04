## happy path 1
* greet: hello there!
    - utter_greet
* mood_great: amazing   <!-- predicted: smalltalk_appraisal_good: amazing -->
    - utter_happy   <!-- predicted: utter_smalltalk_appraisal_good -->


## happy path 2
* greet: hello there!
    - utter_greet
* mood_great: amazing   <!-- predicted: smalltalk_appraisal_good: amazing -->
    - utter_happy   <!-- predicted: utter_smalltalk_appraisal_good -->
* goodbye: bye-bye!   <!-- predicted: smalltalk_greetings_bye: bye-bye! -->
    - utter_goodbye   <!-- predicted: utter_smalltalk_greetings_bye -->


## sad path 1
* greet: hello   <!-- predicted: smalltalk_greetings_hello: hello -->
    - utter_greet   <!-- predicted: utter_smalltalk_greetings_goodnight -->
* mood_unhappy: not good   <!-- predicted: smalltalk_appraisal_bad: not good -->
    - utter_cheer_up   <!-- predicted: utter_smalltalk_appraisal_bad -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* affirm: yes   <!-- predicted: smalltalk_confirmation_yes: yes -->
    - utter_happy   <!-- predicted: utter_smalltalk_confirmation_yes -->


## sad path 2
* greet: hello   <!-- predicted: smalltalk_greetings_hello: hello -->
    - utter_greet   <!-- predicted: utter_smalltalk_greetings_goodnight -->
* mood_unhappy: not good   <!-- predicted: smalltalk_appraisal_bad: not good -->
    - utter_cheer_up   <!-- predicted: utter_smalltalk_appraisal_bad -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* deny: not really   <!-- predicted: smalltalk_confirmation_no: not really -->
    - utter_goodbye   <!-- predicted: utter_smalltalk_confirmation_no -->


## sad path 3
* greet: hi
    - utter_greet
* mood_unhappy: very terrible   <!-- predicted: smalltalk_appraisal_bad: very terrible -->
    - utter_cheer_up   <!-- predicted: utter_smalltalk_appraisal_bad -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* deny: no   <!-- predicted: smalltalk_confirmation_no: no -->
    - utter_goodbye   <!-- predicted: utter_smalltalk_confirmation_no -->


## say goodbye
* goodbye: bye-bye!   <!-- predicted: smalltalk_greetings_bye: bye-bye! -->
    - utter_goodbye   <!-- predicted: utter_smalltalk_greetings_bye -->


## bot challenge
* bot_challenge: are you a bot?   <!-- predicted: smalltalk_agent_chatbot: are you a bot? -->
    - utter_iamabot   <!-- predicted: utter_smalltalk_agent_chatbot -->


