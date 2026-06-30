from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.uuids import normalize_uuid_str

from aiobmsble import BMSInfo, BMSSample, MatcherPattern
from aiobmsble.basebms import BaseBMS

class BMS(BaseBMS):
    """Implementazione BMS per Dyness."""

    INFO: BMSInfo = {
        "default_manufacturer": "Dyness",
        "default_model": "Dyness BMS",
    }

    def __init__(
        self,
        ble_device: BLEDevice,
        keep_alive: bool = True,
        secret: str = "",
        logger_name: str = "",
    ) -> None:
        super().__init__(ble_device, keep_alive, secret, logger_name)

    @staticmethod
    def matcher_dict_list() -> list[MatcherPattern]:
        # Usiamo il MAC Address come identificativo primario e sicuro
        return [{"address": "C5:95:7D:21:8A:3F", "connectable": True}]

    @staticmethod
    def uuid_services() -> tuple[str, ...]:
        return (normalize_uuid_str("6e400001-b5a3-f393-e0a9-e50e24dcca9e"),)

    @staticmethod
    def uuid_rx() -> str:
        return "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    @staticmethod
    def uuid_tx() -> str:
        return "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    async def _fetch_device_info(self) -> BMSInfo:
        return BMSInfo(
            default_manufacturer="Dyness", default_model="Dyness BMS"
        )

    def _notification_handler(
        self, _sender: BleakGATTCharacteristic, data: bytearray
    ) -> None:
        """Gestisce l'arrivo di nuovi dati dal BMS."""
        self._msg = bytes(data)
        self._msg_event.set()

    async def _async_update(self) -> BMSSample:
        """Aggiorna le informazioni dello stato della batteria."""
        # TODO: Qui in futuro manderemo il comando di richiesta dati
        # await self._await_msg(b"<comando_hex>") 
        
        return {
            "voltage": 52.0,
            "current": 0.0,
            "temperature": 25.0,
        }