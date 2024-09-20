import numpy as np


def walsh_matrix(n):
    if n == 1:
        return np.array([[1]])
    else:
        h = walsh_matrix(n // 2)
        matrix = np.vstack((np.hstack((h, h)), np.hstack((h, -h))))
        print(f'\nМатрица Уолша {n}-го уровня:\n{matrix}')
        return matrix


def word_to_binary(word):
    binary_str = ''.join(format(ord(char), '08b') for char in word)
    print(f'\nБинарное представление слова "{word}":\n{binary_str}')
    return binary_str


def binary_to_word(binary_str):
    chars = [chr(int(binary_str[i:i + 8], 2)) for i in range(0, len(binary_str), 8)]
    print(f'\nРасшфировка последовательности "{binary_str}":\n{''.join(chars)}')
    return ''.join(chars)


def encode_message(message, walsh_code):
    message_bin = word_to_binary(message)
    encoded_message = []
    for bit in message_bin:
        if bit == '1':
            encoded_message.extend(walsh_code)
        else:
            encoded_message.extend(-walsh_code)
    return np.array(encoded_message)


def decode_message(signal, walsh_code):
    n = len(walsh_code)
    decoded_bits = []
    for i in range(0, len(signal), n):
        block = signal[i:i + n]
        decoded_bit = 1 if np.dot(block, walsh_code) > 0 else 0
        decoded_bits.append(decoded_bit)

    decoded_bin = ''.join(map(str, decoded_bits))
    return binary_to_word(decoded_bin)


def main():
    stations = {
        'A': "GOD",
        'B': "CAT",
        'C': "HAM",
        'D': "SUN"
    }

    n = 8
    walsh_codes = walsh_matrix(n)

    encoded_signals = []
    for i, (station, word) in enumerate(stations.items()):
        encoded_signals.append(encode_message(word, walsh_codes[i]))

    combined_signal = np.sum(encoded_signals, axis=0)

    for i, (station, word) in enumerate(stations.items()):
        decoded_message = decode_message(combined_signal, walsh_codes[i])
        print(f"Станция {station}: {decoded_message}")


if __name__ == "__main__":
    main()
