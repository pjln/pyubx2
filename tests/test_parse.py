"""
Parse method tests for pyubx2.UBXMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, VALCKSUM, VALNONE, SET


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ack_ack = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38"
        self.ack_ack_badck = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37"
        self.cfg_msg = b"\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036"
        self.cfg_prt = b"\xb5b\x06\x00\x00\x00\x06\x18"
        self.nav_velned = b"\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6"
        self.nav_svinfo = b""
        self.cfg_nmeavx = b"\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9"
        self.cfg_nmeav0 = b"\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61"
        self.mga_dbd = b"\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2"
        self.mga_flash_ack = b"\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a"
        self.cfg_valget = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0"
        self.cfg_valget2 = (
            b"\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2"
        )
        self.cfg_valget3 = b"\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92"
        self.cfg_valget4 = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d"
        self.esf_meas = b"\xb5b\x10\x02\x10\x00\x01\x02\x03\x04\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x50\x8a"
        self.esf_measct = b"\xb5b\x10\x02\x14\x00\x01\x02\x03\x04\x00\x08\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x66\xae"
        self.esf_meas_log = [
            b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c",
            b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51",
            b"\xb5b\x10\x02\x18\x00\xd5\xd8\x07\x00\x18\x18\x00\x00\x4d\xfd\xff\x10\x45\x02\x00\x11\x1f\x28\x00\x12\xd5\xd8\x07\x00\xcc\xac",
            b"\xb5b\x10\x02\x1c\x00\xd0\xd8\x07\x00\x18\x20\x00\x00\x7c\x06\x00\x0e\xcb\xfe\xff\x0d\xac\xf9\xff\x05\x09\x0b\x00\x0c\xd0\xd8\x07\x00\xf2\xae",
            b"\xb5b\x10\x02\x18\x00\x38\xd9\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x41\x02\x00\x11\x27\x28\x00\x12\x38\xd9\x07\x00\x95\x7a",
            b"\xb5b\x10\x02\x1c\x00\x33\xd9\x07\x00\x18\x20\x00\x00\x0f\x06\x00\x0e\x16\xfe\xff\x0d\x5b\xfa\xff\x05\x0a\x0b\x00\x0c\x33\xd9\x07\x00\x49\x9f",
            b"\xb5b\x10\x02\x18\x00\x9c\xd9\x07\x00\x18\x18\x00\x00\x4e\xfd\xff\x10\x4e\x02\x00\x11\x20\x28\x00\x12\x9c\xd9\x07\x00\x67\x0e",
            b"\xb5b\x10\x02\x1c\x00\x97\xd9\x07\x00\x18\x20\x00\x00\x85\x06\x00\x0e\x77\xfe\xff\x0d\xe1\xf9\xff\x05\x0a\x0b\x00\x0c\x97\xd9\x07\x00\x6d\xa4",
            b"\xb5b\x10\x02\x18\x00\xff\xd9\x07\x00\x18\x18\x00\x00\x4c\xfd\xff\x10\x3e\x02\x00\x11\x24\x28\x00\x12\xff\xd9\x07\x00\x1f\x22",
            b"\xb5b\x10\x02\x1c\x00\xfa\xd9\x07\x00\x18\x20\x00\x00\x92\x06\x00\x0e\x61\xfe\xff\x0d\x9f\xf9\xff\x05\x0a\x0b\x00\x0c\xfa\xd9\x07\x00\xe8\x90",
            b"\xb5b\x10\x02\x18\x00\x63\xda\x07\x00\x18\x18\x00\x00\x47\xfd\xff\x10\x44\x02\x00\x11\x1c\x28\x00\x12\x63\xda\x07\x00\xe2\xe4",
            b"\xb5b\x10\x02\x1c\x00\x5e\xda\x07\x00\x18\x20\x00\x00\xef\x06\x00\x0e\xb8\xfe\xff\x0d\xc8\xf9\xff\x05\x0a\x0b\x00\x0c\x5e\xda\x07\x00\x8f\xce",
            b"\xb5b\x10\x02\x18\x00\xc6\xda\x07\x00\x18\x18\x00\x00\x4a\xfd\xff\x10\x4e\x02\x00\x11\x21\x28\x00\x12\xc6\xda\x07\x00\xba\x88",
            b"\xb5b\x10\x02\x1c\x00\xc1\xda\x07\x00\x18\x20\x00\x00\x82\x06\x00\x0e\x5b\xfe\xff\x0d\xc8\xf9\xff\x05\x09\x0b\x00\x0c\xc1\xda\x07\x00\x8a\xd2",
            b"\xb5b\x10\x02\x18\x00\x2a\xdb\x07\x00\x18\x18\x00\x00\x48\xfd\xff\x10\x47\x02\x00\x11\x27\x28\x00\x12\x2a\xdb\x07\x00\x81\x4e",
            b"\xb5b\x10\x02\x1c\x00\x25\xdb\x07\x00\x18\x20\x00\x00\x1b\x07\x00\x0e\xed\xfe\xff\x0d\xfa\xf9\xff\x05\x09\x0b\x00\x0c\x25\xdb\x07\x00\xb2\xef",
            b"\xb5b\x10\x02\x1c\x00\xdb\x25\x01\x00\x18\x20\x00\x00\x76\x02\x00\x0e\x06\xf8\xff\x0d\xde\xf7\xff\x05\x54\x0a\x00\x0c\xdb\x25\x01\x00\x3b\x91",
            b"\xb5b\x10\x02\x18\x00\xee\x23\x01\x00\x18\x18\x00\x00\xe8\x11\x00\x10\xfa\x07\x00\x11\xa1\x22\x00\x12\xee\x23\x01\x00\x6e\xf9",
            b"\xb5b\x10\x02\x1c\x00\x94\x21\x01\x00\x18\x20\x00\x00\xff\x05\x00\x0e\xf3\xfe\xff\x0d\x4d\x0b\x00\x05\x51\x0a\x00\x0c\x94\x21\x01\x00\xa5\x52",
        ]
        self.mga_ini1 = b"\xb5b\x13\x40\x14\x00\x01\x00\x01\x02\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x93\xc8"
        self.mon_span = b"\xb5b\n1\x14\x01\x00\x01\x00\x00-+-,+-.,-.+,+.-..-,..//./00203017?9398:L]<@C;H<>=A@BDCGJNQRVY[_cgpqyz\x7f\x84\x8c\x90\x99\xa0\xa7\xae\xb0\xae\xaa\xa7\xa2\x9b\x97\x96\x94\x91\x90\x8e\x8c\x8c\x8c\x8b\x8b\x89\x88\x89\x89\x89\x8b\x88\x89\x8a\x89\x8a\x8a\x89\x8a\x8b\x8a\x8a\x8b\x8b\x8c\x8a\x8a\x8a\x8b\x88\x88\x87\x87\x86\x85\x85\x85\x84\x89\x84\x85\x83\x84\x84\x84\x85\x88\x87\x87\x88\x8a\x8a\x8a\x8a\x8b\x8e\x8c\x8d\x8d\x8f\x8e\x8d\x8f\x8e\x8f\x8f\x8e\x8f\x8f\x90\x91\x92\x93\x93\x93\x95\x94\x94\x94\x94\x95\x94\x95\x93\x93\x91\x92\x93\x92\x94\x95\x94\x95\x97\x97\x98\x97\x94\x90\x8d\x86\x82\x7fyupmg`]VRLEB?=;99665422202101///-//.-0-.-/..--,.-+-,--+.,,--,,-*\x00 \xa1\x07 \xa1\x07\x00@\xc4`^\x0c\x00\x00\x00\x15j"

        self.RTCM = {
                "1006": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x00\xee\x03\x9dA",
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1006)>"),
                "1075": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x003\x04\xe3\xcc", 
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1075)>"),
                "1085": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x00=\x04\xed\xe0", 
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1085)>"),
                "1095": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x00G\x04\xf7\xf4", 
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1095)>"),
                "1115": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x00[\x04\x0b\x1c", 
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1115)>"),
                "1125": (b"\xb5b\x022\x08\x00\x02\x04\x00\x00j\x00e\x04\x150", 
                    "<UBX(RXM-RTCM, version=2, flags=b'\\x04', subType=0, refStation=106, msgType=1125)>")
        }

    def tearDown(self):
        pass

    def testAck(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testAckID(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(res.identity, "ACK-ACK")

    def testAckStr(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>")

    def testAckRepr(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(
            repr(res), "UBXMessage(b'\\x05', b'\\x01', 0, payload=b'\\x06\\x01')"
        )

    def testAckCkF(self):
        UBXReader.parse(self.ack_ack_badck, validate=VALNONE)

    def testCfg(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertIsInstance(res, UBXMessage)

    def testCfgID(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.identity, "CFG-MSG")

    def testCfgStr(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(
            str(res),
            "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>",
        )

    def testCfgRepr(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x06', b'\\x01', 0, payload=b'\\xf0\\x01\\x00\\x01\\x01\\x01\\x00\\x00')",
        )

    def testCfgProp1(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.rateUART1, 1)

    def testCfgProp2(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(res.rateSPI, 0)

    def testNavVelNed(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testNavVelNedID(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.identity, "NAV-VELNED")

    def testNavVelNedStr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            str(res),
            "<UBX(NAV-VELNED, iTOW=16:01:50, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=128387, sAcc=65, cAcc=8052720)>",
        )

    def testNavVelNedRepr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x01', b'\\x12', 0, payload=b'0D\\n\\x18\\xfd\\xff\\xff\\xff\\xf1\\xff\\xff\\xff\\xfc\\xff\\xff\\xff\\x10\\x00\\x00\\x00\\x0f\\x00\\x00\\x00\\x83\\xf5\\x01\\x00A\\x00\\x00\\x00\\xf0\\xdfz\\x00')",
        )

    def testNavVelNedProp1(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertEqual(res.iTOW, 403326000)

    def testNavVelNedProp2(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.cAcc, 8052720)

    def testCfgPrt(self):  # POLL example with null payload
        res = UBXReader.parse(self.cfg_prt)
        self.assertIsInstance(res, UBXMessage)

    def testCfgPrtID(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(res.identity, "CFG-PRT")

    def testCfgPrtStr(self):
        res = UBXReader.parse(self.cfg_prt, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(CFG-PRT)>")

    def testCfgPrtRepr(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(repr(res), "UBXMessage(b'\\x06', b'\\x00', 0)")

    def testCfgNmeaVx(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeavx)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=0, numSV=0, flags=b'\\x00')>",
        )

    def testCfgNmeaV0(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeav0)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=0, numSV=0, flags=b'\\x00', gnssToFilter=b'\\x00\\x00\\x00\\x00', svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0)>",
        )

    def testMgaDbd(self):
        res = UBXReader.parse(self.mga_dbd)
        self.assertEqual(
            str(res),
            "<UBX(MGA-DBD, reserved1=3727165692135864801209549313, data_01=1, data_02=2)>",
        )

    def testMgaFlashAck(self):
        res = UBXReader.parse(self.mga_flash_ack)
        self.assertEqual(
            str(res),
            "<UBX(MGA-FLASH-ACK, type=3, version=1, ack=2, reserved1=0, sequence=1024)>",
        )

    def testCFGVALGET(self):  # test parser of CFG-VALGET CFG-UART1-BAUDRATE
        res = UBXReader.parse(self.cfg_valget)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_UART1_BAUDRATE=9600)>",
        )

    def testCFGVALGET2(self):  # test parse of CFG-VALGET CFG-I2C-ADDRESS
        res = UBXReader.parse(self.cfg_valget2)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85)>",
        )

    def testCFGVALGET3(
        self,
    ):  # test parse of CFG-VALGET CFG-I2C-ADDRESS, CFG-UART1-BAUDRATE, CFG-RATE-NAV
        res = UBXReader.parse(self.cfg_valget3)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85, CFG_UART1_BAUDRATE=9600, CFG_RATE_NAV=35)>",
        )

    def testCFGVALGET4(self):  # test parser of CFG-VALGET CFG-NAVSPG-USRDAT_ROTY
        res = UBXReader.parse(self.cfg_valget4)
        self.assertAlmostEqual(res.CFG_NAVSPG_USRDAT_ROTY, 1.23, 2)

    def testESFMEAS(self):  # test parser of ESF-MEAS without calibTtag data
        res = UBXReader.parse(self.esf_meas)
        self.assertEqual(
            str(res),
            "<UBX(ESF-MEAS, timeTag=67305985, flags=b'\\x00\\x00', id=0, data_01=b'\\x01\\x02\\x03\\x04', data_02=b'\\x05\\x06\\x07\\x08')>",
        )

    def testESFMEASCT(self):  # test parser of ESF-MEAS with calibTtag data
        res = UBXReader.parse(self.esf_measct)
        self.assertEqual(
            str(res),
            "<UBX(ESF-MEAS, timeTag=67305985, flags=b'\\x00\\x08', id=0, data_01=b'\\x01\\x02\\x03\\x04', data_02=b'\\x05\\x06\\x07\\x08', calibTtag=67305985)>",
        )

    def testESFMEASLOG(
        self,
    ):  # test parse of actual ESF-MEAS log - thanks to tgalecki for log
        EXPECTED_RESULT = [
            "<UBX(ESF-MEAS, timeTag=514162, flags=b'\\x18\\x18', id=0, data_01=b'K\\xfd\\xff\\x10', data_02=b'@\\x02\\x00\\x11', data_03=b'#(\\x00\\x12', calibTtag=514162)>",
            "<UBX(ESF-MEAS, timeTag=514157, flags=b'\\x18 ', id=0, data_01=b'\\xcd\\x06\\x00\\x0e', data_02=b'\\xe4\\xfe\\xff\\r', data_03=b'\\x03\\xfa\\xff\\x05', data_04=b'\\t\\x0b\\x00\\x0c', data_05=b'm\\xd8\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514261, flags=b'\\x18\\x18', id=0, data_01=b'M\\xfd\\xff\\x10', data_02=b'E\\x02\\x00\\x11', data_03=b'\\x1f(\\x00\\x12', calibTtag=514261)>",
            "<UBX(ESF-MEAS, timeTag=514256, flags=b'\\x18 ', id=0, data_01=b'|\\x06\\x00\\x0e', data_02=b'\\xcb\\xfe\\xff\\r', data_03=b'\\xac\\xf9\\xff\\x05', data_04=b'\\t\\x0b\\x00\\x0c', data_05=b'\\xd0\\xd8\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514360, flags=b'\\x18\\x18', id=0, data_01=b'J\\xfd\\xff\\x10', data_02=b'A\\x02\\x00\\x11', data_03=b\"'(\\x00\\x12\", calibTtag=514360)>",
            "<UBX(ESF-MEAS, timeTag=514355, flags=b'\\x18 ', id=0, data_01=b'\\x0f\\x06\\x00\\x0e', data_02=b'\\x16\\xfe\\xff\\r', data_03=b'[\\xfa\\xff\\x05', data_04=b'\\n\\x0b\\x00\\x0c', data_05=b'3\\xd9\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514460, flags=b'\\x18\\x18', id=0, data_01=b'N\\xfd\\xff\\x10', data_02=b'N\\x02\\x00\\x11', data_03=b' (\\x00\\x12', calibTtag=514460)>",
            "<UBX(ESF-MEAS, timeTag=514455, flags=b'\\x18 ', id=0, data_01=b'\\x85\\x06\\x00\\x0e', data_02=b'w\\xfe\\xff\\r', data_03=b'\\xe1\\xf9\\xff\\x05', data_04=b'\\n\\x0b\\x00\\x0c', data_05=b'\\x97\\xd9\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514559, flags=b'\\x18\\x18', id=0, data_01=b'L\\xfd\\xff\\x10', data_02=b'>\\x02\\x00\\x11', data_03=b'$(\\x00\\x12', calibTtag=514559)>",
            "<UBX(ESF-MEAS, timeTag=514554, flags=b'\\x18 ', id=0, data_01=b'\\x92\\x06\\x00\\x0e', data_02=b'a\\xfe\\xff\\r', data_03=b'\\x9f\\xf9\\xff\\x05', data_04=b'\\n\\x0b\\x00\\x0c', data_05=b'\\xfa\\xd9\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514659, flags=b'\\x18\\x18', id=0, data_01=b'G\\xfd\\xff\\x10', data_02=b'D\\x02\\x00\\x11', data_03=b'\\x1c(\\x00\\x12', calibTtag=514659)>",
            "<UBX(ESF-MEAS, timeTag=514654, flags=b'\\x18 ', id=0, data_01=b'\\xef\\x06\\x00\\x0e', data_02=b'\\xb8\\xfe\\xff\\r', data_03=b'\\xc8\\xf9\\xff\\x05', data_04=b'\\n\\x0b\\x00\\x0c', data_05=b'^\\xda\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514758, flags=b'\\x18\\x18', id=0, data_01=b'J\\xfd\\xff\\x10', data_02=b'N\\x02\\x00\\x11', data_03=b'!(\\x00\\x12', calibTtag=514758)>",
            "<UBX(ESF-MEAS, timeTag=514753, flags=b'\\x18 ', id=0, data_01=b'\\x82\\x06\\x00\\x0e', data_02=b'[\\xfe\\xff\\r', data_03=b'\\xc8\\xf9\\xff\\x05', data_04=b'\\t\\x0b\\x00\\x0c', data_05=b'\\xc1\\xda\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=514858, flags=b'\\x18\\x18', id=0, data_01=b'H\\xfd\\xff\\x10', data_02=b'G\\x02\\x00\\x11', data_03=b\"'(\\x00\\x12\", calibTtag=514858)>",
            "<UBX(ESF-MEAS, timeTag=514853, flags=b'\\x18 ', id=0, data_01=b'\\x1b\\x07\\x00\\x0e', data_02=b'\\xed\\xfe\\xff\\r', data_03=b'\\xfa\\xf9\\xff\\x05', data_04=b'\\t\\x0b\\x00\\x0c', data_05=b'%\\xdb\\x07\\x00')>",
            "<UBX(ESF-MEAS, timeTag=75227, flags=b'\\x18 ', id=0, data_01=b'v\\x02\\x00\\x0e', data_02=b'\\x06\\xf8\\xff\\r', data_03=b'\\xde\\xf7\\xff\\x05', data_04=b'T\\n\\x00\\x0c', data_05=b'\\xdb%\\x01\\x00')>",
            "<UBX(ESF-MEAS, timeTag=74734, flags=b'\\x18\\x18', id=0, data_01=b'\\xe8\\x11\\x00\\x10', data_02=b'\\xfa\\x07\\x00\\x11', data_03=b'\\xa1\"\\x00\\x12', calibTtag=74734)>",
            "<UBX(ESF-MEAS, timeTag=74132, flags=b'\\x18 ', id=0, data_01=b'\\xff\\x05\\x00\\x0e', data_02=b'\\xf3\\xfe\\xff\\r', data_03=b'M\\x0b\\x00\\x05', data_04=b'Q\\n\\x00\\x0c', data_05=b'\\x94!\\x01\\x00')>",
        ]
        for i, msg in enumerate(self.esf_meas_log):
            res = UBXReader.parse(msg, validate=VALCKSUM)
            self.assertEqual(str(res), EXPECTED_RESULT[i])

    def testRXMPMPV0(self):  # test parser of RXM-PMP v0 message
        rxm_pmpv0 = b"\xb5b\x02\x72\x0e\x02\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x01\x01"
        for i in range(504):
            n = i % 256
            rxm_pmpv0 += n.to_bytes(1, "little", signed=False)
        rxm_pmpv0 += b"\x01\x02\x01\x00\xcf\xa9"
        res = UBXReader.parse(rxm_pmpv0, validate=VALCKSUM)
        self.assertEqual(
            str(res),
            "<UBX(RXM-PMP, version=0, reserved0=0, timeTag=67305985, uniqueWord1=67305985, uniqueWord2=67305985, serviceIdentifier=513, spare=1, uniqueWordBitErrors=1, userData_01=0, userData_02=1, userData_03=2, userData_04=3, userData_05=4, userData_06=5, userData_07=6, userData_08=7, userData_09=8, userData_10=9, userData_11=10, userData_12=11, userData_13=12, userData_14=13, userData_15=14, userData_16=15, userData_17=16, userData_18=17, userData_19=18, userData_20=19, userData_21=20, userData_22=21, userData_23=22, userData_24=23, userData_25=24, userData_26=25, userData_27=26, userData_28=27, userData_29=28, userData_30=29, userData_31=30, userData_32=31, userData_33=32, userData_34=33, userData_35=34, userData_36=35, userData_37=36, userData_38=37, userData_39=38, userData_40=39, userData_41=40, userData_42=41, userData_43=42, userData_44=43, userData_45=44, userData_46=45, userData_47=46, userData_48=47, userData_49=48, userData_50=49, userData_51=50, userData_52=51, userData_53=52, userData_54=53, userData_55=54, userData_56=55, userData_57=56, userData_58=57, userData_59=58, userData_60=59, userData_61=60, userData_62=61, userData_63=62, userData_64=63, userData_65=64, userData_66=65, userData_67=66, userData_68=67, userData_69=68, userData_70=69, userData_71=70, userData_72=71, userData_73=72, userData_74=73, userData_75=74, userData_76=75, userData_77=76, userData_78=77, userData_79=78, userData_80=79, userData_81=80, userData_82=81, userData_83=82, userData_84=83, userData_85=84, userData_86=85, userData_87=86, userData_88=87, userData_89=88, userData_90=89, userData_91=90, userData_92=91, userData_93=92, userData_94=93, userData_95=94, userData_96=95, userData_97=96, userData_98=97, userData_99=98, userData_100=99, userData_101=100, userData_102=101, userData_103=102, userData_104=103, userData_105=104, userData_106=105, userData_107=106, userData_108=107, userData_109=108, userData_110=109, userData_111=110, userData_112=111, userData_113=112, userData_114=113, userData_115=114, userData_116=115, userData_117=116, userData_118=117, userData_119=118, userData_120=119, userData_121=120, userData_122=121, userData_123=122, userData_124=123, userData_125=124, userData_126=125, userData_127=126, userData_128=127, userData_129=128, userData_130=129, userData_131=130, userData_132=131, userData_133=132, userData_134=133, userData_135=134, userData_136=135, userData_137=136, userData_138=137, userData_139=138, userData_140=139, userData_141=140, userData_142=141, userData_143=142, userData_144=143, userData_145=144, userData_146=145, userData_147=146, userData_148=147, userData_149=148, userData_150=149, userData_151=150, userData_152=151, userData_153=152, userData_154=153, userData_155=154, userData_156=155, userData_157=156, userData_158=157, userData_159=158, userData_160=159, userData_161=160, userData_162=161, userData_163=162, userData_164=163, userData_165=164, userData_166=165, userData_167=166, userData_168=167, userData_169=168, userData_170=169, userData_171=170, userData_172=171, userData_173=172, userData_174=173, userData_175=174, userData_176=175, userData_177=176, userData_178=177, userData_179=178, userData_180=179, userData_181=180, userData_182=181, userData_183=182, userData_184=183, userData_185=184, userData_186=185, userData_187=186, userData_188=187, userData_189=188, userData_190=189, userData_191=190, userData_192=191, userData_193=192, userData_194=193, userData_195=194, userData_196=195, userData_197=196, userData_198=197, userData_199=198, userData_200=199, userData_201=200, userData_202=201, userData_203=202, userData_204=203, userData_205=204, userData_206=205, userData_207=206, userData_208=207, userData_209=208, userData_210=209, userData_211=210, userData_212=211, userData_213=212, userData_214=213, userData_215=214, userData_216=215, userData_217=216, userData_218=217, userData_219=218, userData_220=219, userData_221=220, userData_222=221, userData_223=222, userData_224=223, userData_225=224, userData_226=225, userData_227=226, userData_228=227, userData_229=228, userData_230=229, userData_231=230, userData_232=231, userData_233=232, userData_234=233, userData_235=234, userData_236=235, userData_237=236, userData_238=237, userData_239=238, userData_240=239, userData_241=240, userData_242=241, userData_243=242, userData_244=243, userData_245=244, userData_246=245, userData_247=246, userData_248=247, userData_249=248, userData_250=249, userData_251=250, userData_252=251, userData_253=252, userData_254=253, userData_255=254, userData_256=255, userData_257=0, userData_258=1, userData_259=2, userData_260=3, userData_261=4, userData_262=5, userData_263=6, userData_264=7, userData_265=8, userData_266=9, userData_267=10, userData_268=11, userData_269=12, userData_270=13, userData_271=14, userData_272=15, userData_273=16, userData_274=17, userData_275=18, userData_276=19, userData_277=20, userData_278=21, userData_279=22, userData_280=23, userData_281=24, userData_282=25, userData_283=26, userData_284=27, userData_285=28, userData_286=29, userData_287=30, userData_288=31, userData_289=32, userData_290=33, userData_291=34, userData_292=35, userData_293=36, userData_294=37, userData_295=38, userData_296=39, userData_297=40, userData_298=41, userData_299=42, userData_300=43, userData_301=44, userData_302=45, userData_303=46, userData_304=47, userData_305=48, userData_306=49, userData_307=50, userData_308=51, userData_309=52, userData_310=53, userData_311=54, userData_312=55, userData_313=56, userData_314=57, userData_315=58, userData_316=59, userData_317=60, userData_318=61, userData_319=62, userData_320=63, userData_321=64, userData_322=65, userData_323=66, userData_324=67, userData_325=68, userData_326=69, userData_327=70, userData_328=71, userData_329=72, userData_330=73, userData_331=74, userData_332=75, userData_333=76, userData_334=77, userData_335=78, userData_336=79, userData_337=80, userData_338=81, userData_339=82, userData_340=83, userData_341=84, userData_342=85, userData_343=86, userData_344=87, userData_345=88, userData_346=89, userData_347=90, userData_348=91, userData_349=92, userData_350=93, userData_351=94, userData_352=95, userData_353=96, userData_354=97, userData_355=98, userData_356=99, userData_357=100, userData_358=101, userData_359=102, userData_360=103, userData_361=104, userData_362=105, userData_363=106, userData_364=107, userData_365=108, userData_366=109, userData_367=110, userData_368=111, userData_369=112, userData_370=113, userData_371=114, userData_372=115, userData_373=116, userData_374=117, userData_375=118, userData_376=119, userData_377=120, userData_378=121, userData_379=122, userData_380=123, userData_381=124, userData_382=125, userData_383=126, userData_384=127, userData_385=128, userData_386=129, userData_387=130, userData_388=131, userData_389=132, userData_390=133, userData_391=134, userData_392=135, userData_393=136, userData_394=137, userData_395=138, userData_396=139, userData_397=140, userData_398=141, userData_399=142, userData_400=143, userData_401=144, userData_402=145, userData_403=146, userData_404=147, userData_405=148, userData_406=149, userData_407=150, userData_408=151, userData_409=152, userData_410=153, userData_411=154, userData_412=155, userData_413=156, userData_414=157, userData_415=158, userData_416=159, userData_417=160, userData_418=161, userData_419=162, userData_420=163, userData_421=164, userData_422=165, userData_423=166, userData_424=167, userData_425=168, userData_426=169, userData_427=170, userData_428=171, userData_429=172, userData_430=173, userData_431=174, userData_432=175, userData_433=176, userData_434=177, userData_435=178, userData_436=179, userData_437=180, userData_438=181, userData_439=182, userData_440=183, userData_441=184, userData_442=185, userData_443=186, userData_444=187, userData_445=188, userData_446=189, userData_447=190, userData_448=191, userData_449=192, userData_450=193, userData_451=194, userData_452=195, userData_453=196, userData_454=197, userData_455=198, userData_456=199, userData_457=200, userData_458=201, userData_459=202, userData_460=203, userData_461=204, userData_462=205, userData_463=206, userData_464=207, userData_465=208, userData_466=209, userData_467=210, userData_468=211, userData_469=212, userData_470=213, userData_471=214, userData_472=215, userData_473=216, userData_474=217, userData_475=218, userData_476=219, userData_477=220, userData_478=221, userData_479=222, userData_480=223, userData_481=224, userData_482=225, userData_483=226, userData_484=227, userData_485=228, userData_486=229, userData_487=230, userData_488=231, userData_489=232, userData_490=233, userData_491=234, userData_492=235, userData_493=236, userData_494=237, userData_495=238, userData_496=239, userData_497=240, userData_498=241, userData_499=242, userData_500=243, userData_501=244, userData_502=245, userData_503=246, userData_504=247, fecBits=513, ebno=1, reserved1=0)>",
        )

    def testRXMPMPV1(self):  # test parser of RXM-PMP v1 message
        rxm_pmpv1 = b"\xb5b\x02\x72\x23\x00\x01\x00\x0b\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x00\x01\x01\x02\x01\x00"
        for i in range(11):
            rxm_pmpv1 += i.to_bytes(1, "little", signed=False)
        rxm_pmpv1 += b"\x00\x20"
        res = UBXReader.parse(rxm_pmpv1, True)
        self.assertEqual(
            str(res),
            "<UBX(RXM-PMP, version=1, reserved0=0, numBytesUserData=11, timeTag=67305985, uniqueWord1=67305985, uniqueWord2=67305985, serviceIdentifier=513, spare=0, uniqueWordBitErrors=1, fecBits=513, ebno=1, reserved1=0, userData_01=0, userData_02=1, userData_03=2, userData_04=3, userData_05=4, userData_06=5, userData_07=6, userData_08=7, userData_09=8, userData_10=9, userData_11=10)>",
        )

    def testRXMRLMS(self):  # test parser of RXM-RLM-S message
        rxm_rlms = b"\xb5b\x02\x59\x10\x00\x00\x01\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\x00\x8b\xbd"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=1, svId=0, reserved0=0, beacon_01=0, beacon_02=1, beacon_03=2, beacon_04=3, beacon_05=4, beacon_06=5, beacon_07=6, beacon_08=7, message=0, params1=1, params2=2, reserved1=0)>",
        )

    def testRXMRLML(self):  # test parser of RXM-RLM-L message
        rxm_rlms = b"\xb5b\x02\x59\x1c\x00\x00\x02\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00"
        for i in range(12):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\xda\x81"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=2, svId=0, reserved0=0, beacon_01=0, beacon_02=1, beacon_03=2, beacon_04=3, beacon_05=4, beacon_06=5, beacon_07=6, beacon_08=7, message=0, params_01=0, params_02=1, params_03=2, params_04=3, params_05=4, params_06=5, params_07=6, params_08=7, params_09=8, params_10=9, params_11=10, params_12=11, reserved1=131328)>",
        )

    def testMONSPAN(self):  # test parser of MON-SPAN message
        res = UBXReader.parse(self.mon_span)
        self.assertEqual(
            str(res),
            "<UBX(MON-SPAN, version=0, numRfBlocks=1, reserved0=0, spectrum_01=[45, 43, 45, 44, 43, 45, 46, 44, 45, 46, 43, 44, 43, 46, 45, 46, 46, 45, 44, 46, 46, 47, 47, 46, 47, 48, 48, 50, 48, 51, 48, 49, 55, 63, 57, 51, 57, 56, 58, 76, 93, 60, 64, 67, 59, 72, 60, 62, 61, 65, 64, 66, 68, 67, 71, 74, 78, 81, 82, 86, 89, 91, 95, 99, 103, 112, 113, 121, 122, 127, 132, 140, 144, 153, 160, 167, 174, 176, 174, 170, 167, 162, 155, 151, 150, 148, 145, 144, 142, 140, 140, 140, 139, 139, 137, 136, 137, 137, 137, 139, 136, 137, 138, 137, 138, 138, 137, 138, 139, 138, 138, 139, 139, 140, 138, 138, 138, 139, 136, 136, 135, 135, 134, 133, 133, 133, 132, 137, 132, 133, 131, 132, 132, 132, 133, 136, 135, 135, 136, 138, 138, 138, 138, 139, 142, 140, 141, 141, 143, 142, 141, 143, 142, 143, 143, 142, 143, 143, 144, 145, 146, 147, 147, 147, 149, 148, 148, 148, 148, 149, 148, 149, 147, 147, 145, 146, 147, 146, 148, 149, 148, 149, 151, 151, 152, 151, 148, 144, 141, 134, 130, 127, 121, 117, 112, 109, 103, 96, 93, 86, 82, 76, 69, 66, 63, 61, 59, 57, 57, 54, 54, 53, 52, 50, 50, 50, 48, 50, 49, 48, 49, 47, 47, 47, 45, 47, 47, 46, 45, 48, 45, 46, 45, 47, 46, 46, 45, 45, 44, 46, 45, 43, 45, 44, 45, 45, 43, 46, 44, 44, 45, 45, 44, 44, 45, 42], span_01=128000000, res_01=500000, center_01=1583400000, pga_01=12, reserved1_01=0)>",
        )

    def testMONSPAN2(self):  # test parser of MON-SPAN message (repeating groups empty)
        mon_span = b"\xb5b\x0a\x31\x04\x00\x00\x00\x01\x02"
        mon_span += b"\x42\xc3"
        res = UBXReader.parse(mon_span)
        self.assertEqual(
            str(res), "<UBX(MON-SPAN, version=0, numRfBlocks=0, reserved0=513)>"
        )

    def testMGAINI1(self):  # test parser of MGA-INI input message with kwargs
        res = UBXReader.parse(self.mga_ini1, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS_LLH, type=1, version=0, reserved1=513, lat=67305985, lon=67305985, alt=67305985, posAcc=67305985)>",
        )

    def testMGAINI2(self):  # test parser of MGA-INI input message with args
        res = UBXReader.parse(self.mga_ini1, True, SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS_LLH, type=1, version=0, reserved1=513, lat=67305985, lon=67305985, alt=67305985, posAcc=67305985)>",
        )

    def testRTCM(self): # test parser of RTCM-3X messages
        for item in self.RTCM.values():
            res = UBXReader.parse(item[0])
            self.assertEqual(str(res), item[1])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
