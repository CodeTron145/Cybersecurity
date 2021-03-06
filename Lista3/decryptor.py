from dataclasses import dataclass, field
from operator import itemgetter
from typing import Dict, List


@dataclass(frozen=True)
class Polish:
    frequency: Dict[str, float] = field(
        default_factory=lambda: {
            "i": 8.83,
            "e": 8.68,
            "a": 8.37,
            "o": 7.53,
            "n": 5.69,
            "z": 5.33,
            "r": 4.15,
            "s": 4.13,
            "w": 4.11,
            "y": 4.03,
            "c": 3.89,
            "t": 3.85,
            "d": 3.35,
            "k": 3.01,
            "p": 2.87,
            "m": 2.81,
            "ł": 2.38,
            "j": 2.28,
            "l": 2.24,
            "u": 2.06,
            "b": 1.93,
            "g": 1.46,
            "h": 1.25,
            "ę": 1.13,
            "ż": 0.93,
            "ą": 0.79,
            "ó": 0.79,
            "ś": 0.72,
            "ć": 0.60,
            "f": 0.26,
            "ń": 0.16,
            "ź": 0.08,
            " ": 10,
            ",": 1.6,
            ".": 1.0,
            "-": 1.0,
            '"': 1.0,
            "!": 1.0,
            "?": 1.0,
            ":": 1.0,
            ";": 1.0,
            "(": 1.0,
            ")": 1.0,
        }
    )


class Cryptogram:
    def __init__(self, encrypted_bin):
        self.bytes = [
            int(byte, 2) for byte in encrypted_bin.split(" ")
        ]
        self.chars = [chr(byte) for byte in self.bytes]


class Decryptor:
    def __init__(self, path: str = "cryptograms", crypto_count=20):
        self.lang = Polish()
        self.cryptograms = []
        with open(path, "r") as file:
            for ln, line in enumerate(file):
                if ln == crypto_count:
                    break
                self.cryptograms.append(Cryptogram(line))
        self.max_cryptogram_len = len(
            max(self.cryptograms, key=lambda c: len(c.chars)).chars
        )

    def get_key(self):
        key = []

        for n in range(0, self.max_cryptogram_len):
            possible_key = {}

            cur_cryptograms = [
                c for c in self.cryptograms if len(c.bytes) > n
            ]

            for c in cur_cryptograms:
                for letter, frequency in self.lang.frequency.items():
                    tmp = (ord(c.chars[n]) ^ (ord(letter)), frequency)

                    if tmp[0] not in possible_key.keys():
                        possible_key[tmp[0]] = tmp[1]
                    else:
                        possible_key[tmp[0]] = possible_key.get(tmp[0]) + frequency

            tmp_sorted = sorted(possible_key.items(), key=itemgetter(1), reverse=True)
            possible_key = dict(tmp_sorted)

            best_possible = ord(" ")
            best_counter = 0

            for possible in possible_key.keys():
                counter = 0

                for crypt in cur_cryptograms:
                    if (
                        chr(ord(crypt.chars[n]) ^ possible)
                    ) in self.lang.frequency.keys():
                        counter += 1

                if counter > best_counter:
                    best_counter = counter
                    best_possible = possible

            key.append(best_possible)

        return key

    def decrypt(self):
        key = self.get_key()
        for crypt in self.cryptograms:
            result = ""
            for i, char in enumerate(crypt.chars):
                result += chr(ord(char) ^ key[i])
            print(result)


d = Decryptor()
d.decrypt()