pyubx2
=======

`pyubx2` is an original python library for the UBX protocol. 

UBX is a proprietary binary protocol implemented on u-blox &copy; GPS/GNSS receiver modules. At time of writing the library is based
on the [u-blox generation 6 protocol](https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf) but
is readily extensible for later generations.

The `pyubx2` homepage is located at [http://github.com/semuconsulting/pyubx2](http://github.com/semuconsulting/pyubx2).

This is a personal project and I am in no way affiliated with u-blox.

###Current Status

Alpha. Implements the full range of UBX Generation 6 protocol messages *with the exception of* a handful of message classes which
require non-standard processing (AID-ALP, CFG-INF, CFG-RINV, ESF-MEAS). These are in hand.

### Compatibility

`pyubx2` is compatible with Python 3.6+ and has no third-party library dependencies.

![Python version](https://img.shields.io/pypi/pyversions/pyubx2.svg?style=flat)

### Installation

The recommended way to install `pyubx2` is with
[pip](http://pypi.python.org/pypi/pip/):

`pip install pyubx2`

[![PyPI version](https://img.shields.io/pypi/v/pyubx2.svg?style=flat)] (https://pypi.org/project/pyubx2/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyubx2.svg?style=flat)] (https://pypi.org/project/pyubx2/)

##Reading (Streaming)

You can create a `UBXReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual UBX messages can then be read using the `UBXReader.read()` function, which returns both the raw binary
data (as bytes) and the parsed data (as a UBXMessage object). The function is thread-safe in so far as the incoming
data stream object is thread-safe.

##Parsing

You can parse individual UBX messages using the `UBXMessage.parse(data, validate=False)` function, which takes a bytes array containing a
binary UBX message and returns a `UBXMessage` object.

If the optional 'validate' parameter is set to `True`, `parse` will validate the supplied UBX message header, payload length and checksum. 
If any of these are not consistent with the message content, it will raise a `UBXParseError`. Otherwise, the function will automatically
generate the appropriate payload length and checksum.

Example:

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage.parse(b'\xb5b\x05\x00\x02\x00\x06\x01\x0e3', True)
>>> msg
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
>>> msg = pyubx2.UBXMessage.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
>>> msg
<UBX(NAV-VELNED, iTOW=403327000, velN=-1, velE=-21, velD=-4, speed=22, gSpeed=21, heading=128387, sAcc=67, cAcc=8056455)>
```

The `UBXMessage` object exposes different public properties depending on its message type or 'identity',
e.g. the `NAV-POSLLH` message has the following properties:

```python
>>> msg
<UBX(NAV-POSLLH, iTOW=403667000, lon=-21601284, lat=526206345, height=86327, hMSL=37844, HAcc=38885, vAcc=16557)>
>>>msg.identity
'NAV-POSLLH'
>>>msg.lat/10**7, msg.lon/10**7
(52.6206345, -2.1601284)
>>>msg.hMSL/10**3
37.844
```

##Generating

You can create a `UBXMessage` object by calling the constructor with message class, message id, payload and inout parameters.

The 'mode' parameter is an integer flag signifying whether the message payload refers to a: 
* GET message (i.e. *from* the receiver - the default)
* SET message (i.e. *to* the receiver)
* POLL message (i.e. *to* the receiver in anticipation of a response back)

The distinction is necessary because the UBX protocol uses the same message class and id
for all three modes, but with different payloads.

e.g. to generate a outgoing CFG-MSG which polls the 'VTG' NMEA message rate on the current port:

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage(b'\x06', b'\x01', b'\xF0\x05', POLL)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```

The constructor also supports plain text representations of the message class and id, e.g.

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage('CFG','CFG-MSG', b'\xF1\x03', True)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Proprietary, msgID=UBX-03)>
```

##Examples

The following examples can be found in the `\examples` folder:

1. `ubxreaderx.py` illustrates how to implement a threaded serial reader for UBX messages using pyubx2. 

**NB:** If you don't see any incoming data, ensure that your receiver device is configured to output UBX 
protocol data. Some development devices only output NMEA data by default; note that a proprietary NMEA 
`PUBX` message type is *not* the same as a UBX protocol message).

##Extensibility


The UBX protocol is principally defined in the modules `ubxtypes_*.py` as a series of dictionaries. Additional message types 
can be readily added to the appropriate dictionary. Message payload definitions must conform to the following rules:
* attribute names must be unique within each message class
* attribute types must be one of the valid types (I1, U1, etc.)
* repeating groups are defined as nested dicts and must be preceded by an attribute which contains the number of
repeats (see NAV-SVINFO by way of example). If this attribute is named 'numCh', the code will identity it automatically; 
if the attribute is given a different name, ubxmessage.py will need to be modified to identify it explicitly. If such
an attribute is *not* present, the code will need to be modified to handle this particular message type as an exception to
the norm e.g. deduce the number of repeats from the payload length.
* repeating attribute names are suffixed with a two-digit index (svid_01, svid_02, etc.)

## Graphical Client

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols (via pynmea2 and pyubx2 
respectively) is under development at: 

[http://github.com/semuconsulting/PyGPSClient](http://github.com/semuconsulting/PyGPSClient)

## Author Information

semuadmin@semuconsulting.com
 