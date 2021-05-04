class OptionsData:
    
    pay_options = {
        "1":"100€",
        "2":"200€",
        "3":"500€",
        "4":"1000€",
        "5":"2000€"
    }

    taxes_options = {
        "1":"IRPF - Impuesto sobre la Renta de Personas Físicas",
        "2":"IS - Impuesto de Sociedades",
        "3":"Patrimonio - Impuesto sobre Patrimonio",
        "4":"DyS - Donaciones y sucesiones",
        "5":"IVA - Impuesto sobre el Valor añadido",
        "6":"IAE - Impuesto sobre actividades económicas",
        "7":"IBI - Impuesto sobre bienes e inmuebles",
        "8":"IVTM - Impuesto sobre Vehículos de Tracción Mecánica",
    }

    spend_options = {
        "1":"Plan 1 - Mejora de alumbrado público",
        "2":"Plan 2 - Ayudas para material escolar",
        "3":"Plan 3 - Ayudas para comedores sociales",
        "4":"Plan 4 - Creación de nuevas zonas verdes.",
        "5":"Plan 5 - Creación de nuevos carriles bici."
    }

    def add_pay_option(self,option):
        self.pay_options[str(int(self.pay_options.keys()[-1])+1)] = option

    def delete_pay_option(self,index):
        del self.pay_options[index]

    def add_taxes_option(self,option):
        self.taxes_options[str(int(self.taxes_options.keys()[-1])+1)] = option

    def delete_taxes_option(self,index):
        del self.taxes_options[index]

    def add_spend_option(self,option):
        self.spend_options[str(int(self.spend_options.keys()[-1])+1)] = option

    def delete_spend_option(self,index):
        del self.spend_options[index]