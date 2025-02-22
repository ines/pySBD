# -*- coding: utf-8 -*-
import pytest
import pysbd


RULES_TEST_CASES = [
    ("Hello World. My name is Jonas.", ["Hello World.", "My name is Jonas."]),
    ("What is your name? My name is Jonas.", ["What is your name?", "My name is Jonas."]),
    ("There it is! I found it.", ["There it is!", "I found it."]),
    ("My name is Jonas E. Smith.", ["My name is Jonas E. Smith."]),
    ("Please turn to p. 55.", ["Please turn to p. 55."]),
    ("Were Jane and co. at the party?", ["Were Jane and co. at the party?"]),
    ("They closed the deal with Pitt, Briggs & Co. at noon.",
        ["They closed the deal with Pitt, Briggs & Co. at noon."]),
    (
        "Let's ask Jane and co. They should know.",
        ["Let's ask Jane and co.", "They should know."]),
    (
        "They closed the deal with Pitt, Briggs & Co. It closed yesterday.", [
            "They closed the deal with Pitt, Briggs & Co.",
            "It closed yesterday."
        ],
    ),
    ("I can see Mt. Fuji from here.", ["I can see Mt. Fuji from here."]),
    (
        "St. Michael's Church is on 5th st. near the light.",
        ["St. Michael's Church is on 5th st. near the light."],
    ),
    ("That is JFK Jr.'s book.", ["That is JFK Jr.'s book."]),
    ("I visited the U.S.A. last year.", ["I visited the U.S.A. last year."]),
    (
        "I live in the E.U. How about you?",
        ["I live in the E.U.", "How about you?"],
    ),
    (
        "I live in the U.S. How about you?",
        ["I live in the U.S.", "How about you?"],
    ),
    ("I work for the U.S. Government in Virginia.",
        ["I work for the U.S. Government in Virginia."]),
    ("I have lived in the U.S. for 20 years.",
        ["I have lived in the U.S. for 20 years."]),
    # Most difficult sentence to crack
    pytest.param(
         "At 5 a.m. Mr. Smith went to the bank. He left the bank at 6 P.M. Mr. Smith then went to the store.",
         [
             "At 5 a.m. Mr. Smith went to the bank.",
             "He left the bank at 6 P.M.", "Mr. Smith then went to the store."
         ], marks=pytest.mark.xfail),
    ("She has $100.00 in her bag.", ["She has $100.00 in her bag."]),
    ("She has $100.00. It is in her bag.", ["She has $100.00.", "It is in her bag."]),
    ("He teaches science (He previously worked for 5 years as an engineer.) at the local University.",
        ["He teaches science (He previously worked for 5 years as an engineer.) at the local University."]),
    ("Her email is Jane.Doe@example.com. I sent her an email.",
        ["Her email is Jane.Doe@example.com.", "I sent her an email."]),
    ("The site is: https://www.example.50.com/new-site/awesome_content.html. Please check it out.",
        ["The site is: https://www.example.50.com/new-site/awesome_content.html.",
            "Please check it out."]),
    (
        "She turned to him, 'This is great.' she said.",
        ["She turned to him, 'This is great.' she said."],
    ),
    (
        'She turned to him, "This is great." she said.',
        ['She turned to him, "This is great." she said.'],
    ),
    (
        'She turned to him, "This is great." She held the book out to show him.',
        [
            'She turned to him, "This is great."',
            "She held the book out to show him."
        ],
    ),
    ("Hello!! Long time no see.", ["Hello!!", "Long time no see."]),
    ("Hello?? Who is there?", ["Hello??", "Who is there?"]),
    ("Hello!? Is that you?", ["Hello!?", "Is that you?"]),
    ("Hello?! Is that you?", ["Hello?!", "Is that you?"]),
    (
        "1.) The first item 2.) The second item",
        ["1.) The first item", "2.) The second item"],
    ),
    (
        "1.) The first item. 2.) The second item.",
        ["1.) The first item.", "2.) The second item."],
    ),
    (
        "1) The first item 2) The second item",
        ["1) The first item", "2) The second item"],
    ),
    ("1) The first item. 2) The second item.",
        ["1) The first item.", "2) The second item."]),
    (
        "1. The first item 2. The second item",
        ["1. The first item", "2. The second item"],
    ),
    (
        "1. The first item. 2. The second item.",
        ["1. The first item.", "2. The second item."],
    ),
    (
        "• 9. The first item • 10. The second item",
        ["• 9. The first item", "• 10. The second item"],
    ),
    (
        "⁃9. The first item ⁃10. The second item",
        ["⁃9. The first item", "⁃10. The second item"],
    ),
    (
        "a. The first item b. The second item c. The third list item",
        ["a. The first item", "b. The second item", "c. The third list item"],
    ),
    (
        "You can find it at N°. 1026.253.553. That is where the treasure is.",
        [
            "You can find it at N°. 1026.253.553.",
            "That is where the treasure is."
        ],
    ),
    (
        "She works at Yahoo! in the accounting department.",
        ["She works at Yahoo! in the accounting department."],
    ),
    (
        "We make a good team, you and I. Did you see Albert I. Jones yesterday?",
        [
            "We make a good team, you and I.",
            "Did you see Albert I. Jones yesterday?"
        ],
    ),
    (
        "Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”",
        [
            "Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”"
        ],
    ),
    (
        """"Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).""",
        [
            '"Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).'
        ],
    ),
    ("If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . . Next sentence.",
        [
            "If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . .",
            "Next sentence."
        ]),
    (
        "I never meant that.... She left the store.",
        ["I never meant that....", "She left the store."],
    ),
    (
        "I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it.",
        [
            "I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it."
        ],
    ),
    (
        "One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . . The practice was not abandoned. . . .",
        [
            "One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds.",
            ". . . The practice was not abandoned. . . ."
        ],
    )
]


@pytest.mark.parametrize('text,expected_sents', RULES_TEST_CASES)
def test_en_sbd(text, expected_sents):
    """SBD tests from Pragmatic Segmenter"""
    seg = pysbd.Segmenter(language="en", clean=False)
    segments = seg.segment(text)
    assert segments == expected_sents
