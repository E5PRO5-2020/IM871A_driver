"""
First test to do Cyclic redundancy check
on payload received from the IM871A WMBUS dongle.

Extract from WMBUS_HCL_Spec_V1.6.pdf -> (2.3.8):
The CRC computation starts from the Control Field and ends with the last octet of
the Payload Field or Time Stamp Field or RSSI Field.



IM871A uses CRC16-CCITT Polynomial 
G(x) = 1 + x^5 + x^12 + x^16
The Polynomial can be represented in a 16bit int
1000 1000 0001 0001
The IM871A Uses the Reversed version
0010 0000 1101 1000 -> Which gives this hexadecimal representation:
"""
CRC16_POLYNOM = 0x8408

"""
Start value for CRC calculation. 
"""
CRC16_INIT_VALUE = 0xFFFF

"""
Test strings copied from Raspberry Pi terminal.
Testing with bytes and string types.  
"""

payload1 = b'a5820327442d2c5768663230028d20cb103407201d82040f26a7e808ff3449f9e9d2e4b28bd7e7c6f1c6df3885'
payload2 = "a582032d442d2c5768663230028d20cc113407207a8a0a514fee3152ff6b30c18b865e189e5e3ecde8f77142dee93cd4578e2b"
payload3 = b'a5820327442d2c5768663230028d20cd12340720519df247ff65e751662a300bc4e5c67da86477f0182637c1ab'
payload4 = "a5820327442d2c5768663230028d20ce13340720cf5fb58233baa470d6ccabe4d7de2e05ddebb50a60542b0ec3"
payload5 = "a5820327442d2c5768663230028d20cf2034072032eda5bdd17fed4d01fe9cb2a351b33a045fee0331c1b98bd4"
payload6 = "a5820327442d2c5768663230028d20d02134072070e23c59f596a274518adcfac241d567d8c209e7fcb6abc730"
payload7 = "a5820327442d2c5768663230028d20d122340720a46a9ed13fe6bbacf2b623e5c3146e9591496f80422b23c3e6"
payload8 = "a5820327442d2c5768663230028d20d230340720bda38b5c2dd10a0437d21cdc23e6e19983aa2d7d7a91631a58"

" Table to speed up the calculation"
CRC16_TABLE = [0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
               0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
               0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
               0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
               0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
               0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
               0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
               0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
               0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
               0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
               0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
               0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
               0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
               0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
               0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
               0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
               0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
               0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
               0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
               0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
               0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
               0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
               0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
               0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
               0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
               0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
               0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
               0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
               0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
               0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
               0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
               0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78]


def crc16(datagram: bytes, crc: int, table: list) -> int:
    for byte in datagram:
        crc = (crc << 8) ^ table[(crc ^ byte) & 0x00FF]
    return crc


def __crc16_check(cal_crc: int, data_crc: bytes) -> bool:
    if cal_crc == data_crc:
        print("Awesome")
        return True
    print("Just no")
    return False


def crc16_notable(datagram: bytes, crc: int):
    for byte in datagram:
        for bit in range(8):
            if (byte & 1) ^ (crc & 1):
                crc = (crc << 1) ^ CRC16_POLYNOM
            else:
                crc >>= 1
            byte >>= 1
    return crc


def crc16_3rd(datagram: bytes):
    crc = 0xFFFF
    for byte in datagram:
        crc ^= (byte << 8)
        for bit in range(8):
            if (crc & 0x8000) != 0:
                crc = (crc << 1) ^ CRC16_POLYNOM
            else:
                crc <<= 1
    return crc


# calculated_crc = crc16(payload1[:-4], CRC16_INIT_VALUE, CRC16_TABLE)
calculated_crc = crc16_notable(payload1[2:-4], CRC16_INIT_VALUE)
# calculated_crc = crc16_3rd(payload3[2:-4])
print(hex(calculated_crc))
print(payload1[-4:])
