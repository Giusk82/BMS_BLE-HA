from aiobmsble.basebms import BaseBMS
from aiobmsble import MatcherPattern, BMSSample
from bleak.backends.characteristic import BleakGATTCharacteristic

class DynessBMS(BaseBMS):
    def __init__(self, ble_device, keep_alive=True, secret="", logger_name=""):
        super().__init__(ble_device, keep_alive, secret, logger_name)

    @staticmethod
    def matcher_dict_list() -> list[MatcherPattern]:
        # Questo serve ad aiobmsble per capire che questo driver è per Dyness
        # Puoi usare il nome che appare quando scansioni la batteria
        return [{"local_name": "Dyness", "connectable": True}]

    # --- UUIDs ---
    # Questi identificano i canali di comunicazione della batteria.
    # Se il sistema non si connette, probabilmente devi aggiornarli con quelli corretti.
    @staticmethod
    def uuid_services() -> tuple[str, ...]:
        return ("6e400001-b5a3-f393-e0a9-e50e24dcca9e",)

    @staticmethod
    def uuid_rx() -> str:
        return "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    @staticmethod
    def uuid_tx() -> str:
        return "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

    # --- La parte difficile: interpretare i dati ---
    def _notification_handler(self, _sender: BleakGATTCharacteristic, data: bytearray) -> None:
        # Quando la batteria invia dati, arrivano qui come 'data' (in formato esadecimale)
        # Esempio: print(data.hex()) per vedere cosa sta arrivando
        self._msg = bytes(data)
        self._msg_event.set()

    async def _async_update(self) -> BMSSample:
        # Qui devi trasformare i byte in valori reali (Volt, Ampere, SoC).
        # Per ora restituisce valori fissi per verificare che il driver venga caricato.
        return {
            "voltage": 52.0,  # Esempio
            "current": 0.0,
            "temperature": 25.0,
        }