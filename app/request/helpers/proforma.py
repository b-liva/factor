class ProformaSpec:
    @classmethod
    def split_specs_if_profit_exists(cls, specs):
        specs_has_profit = list()
        specs_no_profit = list()
        for spec in specs:
            if spec['profit']:
                specs_has_profit.append(spec)
            else:
                specs_no_profit.append(spec)
        return {
            'specs_has_profit': specs_has_profit,
            'specs_no_profit': specs_no_profit,
        }