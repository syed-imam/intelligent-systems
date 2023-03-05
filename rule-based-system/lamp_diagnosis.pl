:- dynamic(power_failure/1). /* we store the power_failure response in the database to avoid asking it again */
:- dynamic(rules_triggered/1).

/* If the power is on, we check the bulb, otherwise we check the fuse */
check_power :-
    write("Is the power on? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Power on?" + Response)),
    (Response == "yes" -> check_bulb;
     check_fuse).

/* If there is a blown fuse, we check the circuit breaker, otherwise we check for power failure */
check_fuse :-
    write("Is there a blown fuse? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Blown fuse?" + Response)),
    (Response == "yes" -> check_circuit_breaker;
     check_power_failure).

/* If there is a power failure, we wait for power to come back on, otherwise we check the circuit breaker */
check_power_failure :-
    write("Is there a power failure? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Power failure?" + Response)),
    (Response == "yes" -> assertz(power_failure("yes")), write("Wait for power to come back on.");
     check_circuit_breaker).

/* If the circuit breaker is tripped, we reset it, otherwise we check the bulb */
check_circuit_breaker :-
    write("Is the circuit breaker tripped? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Circuit breaker tripped?" + Response)),
    (Response == "yes" -> write("Reset the circuit breaker to fix the problem.");
    power_failure("yes"), !, check_power_failure). /* Reads power_failure from the database if present*/

/* If the bulb is bad, we replace it, otherwise we check the switch */
check_bulb :-
    write("Is the bulb bad? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Bad bulb?" + Response)),
    (Response == "yes" -> write("Replace the bulb to fix the problem.");
    check_switch).

/* If the switch is bad, we replace it, otherwise we check the plug */
check_switch :-
    write("Is the switch bad? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Bad switch?" + Response)),
    (Response == "yes" -> write("Replace the switch to fix the problem.");
     check_plug).

/* If the plug is bad, we replace it, otherwise we check the cord */
check_plug :-
    write("Is the plug bad? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Bad plug?" + Response)),
    (Response == "yes" -> write("Fix or replace the plug to fix the problem.");
     check_cord).

/* If the cord is bad, we replace it, otherwise we check the outlet */
check_cord :-
    write("Is the cord bad? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Bad cord?" + Response)),
    (Response == "yes" -> write("Fix or replace the cord to fix the problem.");
     check_outlet).

/* If the outlet is bad, we replace it, otherwise we check the outlet */
check_outlet :-
    write("Is the wall outlet bad? (yes/no)"),
    read_string(user_input, "\n", "\r",_,Response),
    assertz(rules_triggered("Bad outlet?" + Response)),
    (Response == "yes" -> write("Fix or replace the wall outlet to");
     write("The problem is unknown.")).

print_list :-
    findall(X, rules_triggered(X), List),
    write("\nExplanation of how diagnosis was reached\n"),
    write(List).

/* Starting assumption is that the lamp does not work, we continue to check_power */
go :-
    /* retractall removes all facts from the database */
    retractall(power_failure(_)),
    retractall(rules_triggered(_)),
    write("Lamp does not work."),nl,
    check_power,
    print_list.
go:-
  write('Problem is unknown').
