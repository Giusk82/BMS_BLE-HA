from aiobmsble.basebms import BaseBMS
from aiobmsble import MatcherPattern, BMSSample
from bleak.backends.characteristic import BleakGATTCharacteristic

class DynessBMS(BaseBMS):
    def __init__(self, ble_device, keep_alive=True, secret="", logger_name=""):
        super().__init__(ble_device, keep_alive, secret, logger_name)

    @staticmethod
    def matcher_dict_list() -> list[MatcherPattern]:
        # Aggiornato con il nome esatto rilevato tramite nRF Connect
        return [{"local_name": "DYNWRGBC5957D218A3F", "connectable": True}]

    # --- UUIDs ---
    # Confermati dalla scansione nRF Connect
    @staticmethod
    def uuid_services() -> tuple[str, ...]:
        return ("6e400001-b5a3-f393-e0a9-e50e24dcca9e",)

    @staticmethod
    def uuid_rx() -> str:
        # Caratteristica su cui la batteria invia i dati (Notify)
        return "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    @staticmethod
    def uuid_tx() -> str:
        # Caratteristica su cui inviamo i comandi (Write)
        return "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    # --- Gestione dati ---
    def _notification_handler(self, _sender: BleakGATTCharacteristic, data: bytearray) -> None:
        # Quando la batteria invia dati, li salviamo per l'elaborazione
        self._msg = bytes(data)
        self._msg_event.set()

    async def _async_update(self) -> BMSSample:
        # Per ora restituisce valori fissi per verificare la connessione avvenuta
        return {
            "voltage": 52.0,
            "current": 0.0,
            "temperature": 25.0,
        }