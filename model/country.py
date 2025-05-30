class Country:
    def __init__(self, value, label):
        self.value = value
        self.label = label

    def to_dict(country):
        return {
            "value": country.value,
            "label": country.label
        }

    def from_dict(country_dict):
        return Country(
            value=country_dict.get("value"),
            label=country_dict.get("label")
        )
