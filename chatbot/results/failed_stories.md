## happy path 1
* greet: hello there!
    - utter_greet
* mood_great: amazing   <!-- predicted: greet: amazing -->
    - utter_happy   <!-- predicted: utter_greet -->


## happy path 2
* greet: hello there!
    - utter_greet
* mood_great: amazing   <!-- predicted: greet: amazing -->
    - utter_happy   <!-- predicted: utter_greet -->
* goodbye: bye-bye!
    - utter_goodbye


## sad path 1
* greet: hello
    - utter_greet
* mood_unhappy: not good   <!-- predicted: deny: not good -->
    - utter_cheer_up   <!-- predicted: utter_goodbye -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* affirm: yes
    - utter_happy


## sad path 2
* greet: hello
    - utter_greet
* mood_unhappy: not good   <!-- predicted: deny: not good -->
    - utter_cheer_up   <!-- predicted: utter_goodbye -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* deny: not really
    - utter_goodbye


## sad path 3
* greet: hi
    - utter_greet
* mood_unhappy: very terrible   <!-- predicted: goodbye: very terrible -->
    - utter_cheer_up   <!-- predicted: utter_goodbye -->
    - utter_did_that_help   <!-- predicted: action_listen -->
* deny: no
    - utter_goodbye


## bot challenge
* bot_challenge: are you a bot?   <!-- predicted: goodbye: are you a bot? -->
    - utter_iamabot   <!-- predicted: utter_goodbye -->


