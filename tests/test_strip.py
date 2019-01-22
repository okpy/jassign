from jassign.to_ok import replace_solutions

examples = [
    ((
        "def square(x):\n"
        "    y = x * x # SOLUTION NO PROMPT\n"
        "    return y # SOLUTION\n"
        "\n"
        "nine = square(3) # SOLUTION"
    ), (
        "def square(x):\n"
        "    ...\n"
        "\n"
        "nine = ..."
    )),
    ((
        "pi = 3.14\n"
        "if True:\n"
        "    # BEGIN SOLUTION\n"
        "    radius = 3\n"
        "    area = radius * pi * pi\n"
        "    # END SOLUTION\n"
        "    print('A circle with radius', radius, 'has area', area)\n"
        "def circumference(r):\n"
        "    # BEGIN SOLUTION NO PROMPT\n"
        "    return 2 * pi * r\n"
        "    # END SOLUTION\n"
        "    ''' # BEGIN PROMPT\n"
        "    # Next, define a circumference function.\n"
        "    pass\n"
        "    ''' # END PROMPT"
    ), (
        "pi = 3.14\n"
        "if True:\n"
        "    ...\n"
        "    print('A circle with radius', radius, 'has area', area)\n"
        "def circumference(r):\n"
        "    # Next, define a circumference function.\n"
        "    pass"
    ))
]

def test_replace():
    for original, stripped in examples:
        replaced = replace_solutions(original.split('\n'))
        assert replaced == stripped.split('\n'), replaced