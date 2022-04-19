class ProcessFormData:
    def process_form_data(self, form_data, constants_data):
        self._get_reference_data()

        primary_stone = self._get_primary_stone(form_data, self.primary_reference)
        primary_diamond_addributes = self._get_primary_diamond_attributes(form_data, self.diamond_clarity_reference, self.diamond_color_reference,
                                                                            self.diamond_cut_reference, self.diamond_quality_reference)
        primary_sapphire_attributes = self._get_primary_sapphire_attributes(form_data, self.sapphire_color_reference, self.sapphire_cut_reference)
        primary_garnet_attributes = self._get_primary_garnet_attributes(form_data, self.garnet_color_reference)
        primary_pearl_attributes = self._get_primary_pearl_attributes(form_data, self.pearl_type_reference)
        primary_emerald_attributes = self._get_primary_emerald_attributes(form_data, self.emerald_cut_reference, self.emerald_properties_reference)
        primary_topaz_attributes = self._get_primary_topaz_attributes(form_data, self.topaz_color_reference)
        primary_quartz_attributes = self._get_primary_quartz_attributes(form_data, self.quartz_color_reference)
        secondary_diamonds_attributes = self._get_secondary_diamonds(form_data, self.diamonds_color_reference, self.diamonds_cut_reference)
        secondary_garnets_attributes = self._get_secondary_garnets(form_data, self.garnets_color_reference)
        secondary_sapphires_attributes = self._get_secondary_sapphires(form_data, self.sapphires_color_reference, self.sapphires_cut_reference)
        secondary_mother_of_pearl_attributes = self._get_secondary_mother_of_pearl(form_data, self.mother_of_pearl_color_reference)
        carat_values = self._format_carat_values()
        radio_values = self._get_radio_values()
        additional_values = self._get_additional_options()

    def _get_reference_data(self):
        self.primary_reference = list(constants_data.keys())

        self.diamond_color_reference = constants_data['diamond']['color']
        self.diamond_cut_reference = constants_data['diamond']['cut']
        self.diamond_quality_reference = constants_data['diamond']['quality']
        self.diamond_clarity_reference = constants_data['diamond']['clarity'].remove('OTHER')

        self.sapphire_color_reference = constants_data['sapphire']['color']
        self.sapphire_cut_reference = constants_data['sapphire']['cut']

        self.garnet_color_reference = constants_data['garnet']['color']

        self.pearl_type_reference = constants_data['pearl']['type']

        self.emerald_cut_reference = constants_data['emerald']['cut']
        self.emerald_properties_reference = constants_data['emerald']['properties']

        self.topaz_color_reference = constants_data['topaz']['color']

        self.quartz_color_reference = constants_data['quartz']['color']

        self.diamonds_color_reference = constants_data['diamonds']['color']
        self.diamonds_cut_reference = constants_data['diamonds']['cut']

        self.garnets_color_reference = constants_data['garnet']['color']

        self.sapphires_color_reference = constants_data['sapphires']['color']
        self.sapphires_cut_reference = constants_data['sapphires']['cut']

        self.mother_of_pearl_color_reference = constants_data['mother-of-pearl']['color']

    def _get_value(self, data, id, reference):
        response = data.get(id)
        if response:
            return self._validate_attribute(response, reference)
        else:
            return None
        
    def _get_attribute(self, data, id, default_name, reference):
        response = data.get(id)
        if not (response is None or response == default_name):
            return self._validate_attribute(response, reference)
        else:
            return None

    def _get_carat_attribute(self, data, id, num_type, validation_func):
        carat_value = data.get(id)
        if not carat_value:
            return None
        else:
            try:
               num_val = num_type(carat_value)
               if validation_func(num_val):
                   return num_val
               else:
                   return None
            except ValueError:
                return None

    def _validate_attribute(self, value, reference):
        if isinstance(reference, str):
            if value != reference:
                return None
            else:
                return value
        else:
            if not value in reference:
                return None
            else:
                return value

    def _get_primary_stone(self, data, reference):
        primary_stone = self._get_attribute(data, 'primary-stone', 'none', reference)
        return primary_stone

    def _get_primary_diamond_attributes(self, data, reference_clarity, reference_color, reference_cut, reference_quality):
        primary_diamond_clairy = self._get_attribute(data, 'primary-property-diamond-clarity', 'clarity', reference_clarity)
        primary_diamond_color = self._get_attribute(data, 'primary-property-diamond-color', 'color', reference_color)
        primary_diamond_cut = self._get_attribute(data, 'primary-property-diamond-cut', 'cut', reference_cut)
        primary_diamond_quality = self._get_attribute(data, 'primary-property-diamond-quality', 'quality', reference_quality)

        if primary_diamond_clairy:
            primary_diamond_clairy = map((lambda x: x.lower()), primary_diamond_clairy)
        if primary_diamond_quality:
            primary_diamond_quality = map((lambda x: x.lower()), primary_diamond_quality)
        return primary_diamond_clairy, primary_diamond_color, primary_diamond_cut, primary_diamond_quality

    def _get_primary_emerald_attributes(self, data, reference_cut, reference_properties):
        primary_emerald_cut = self._get_attribute(data, 'primary-property-emerald-cut', 'cut', reference_cut)
        primary_emerald_properties = self._get_attribute(data, 'primary-property-emerald-properties', 'properties', reference_properties)
        return primary_emerald_cut, primary_emerald_properties

    def _get_primary_garnet_attributes(self, data, reference):
        primary_garnet_color = self._get_attribute(data, 'primary-property-garnet-color', 'color', reference)
        return primary_garnet_color

    def _get_primary_pearl_attributes(self, data, reference):
        primary_pearl_type = self._get_attribute(data, 'primary-property-pearl-type', 'type', reference)
        return primary_pearl_type

    def _get_primary_quartz_attributes(self, data, reference):
        primary_quartz_color = self._get_attribute(data, 'primary-property-quartz-color', 'color', reference)
        return primary_quartz_color

    def _get_primary_sapphire_attributes(self, data, reference_color, reference_cut):
        primary_sapphire_color = self._get_attribute(data, 'primary-property-sapphire-color', 'color', reference_color)
        primary_sapphire_cut = self._get_attribute(data, 'primary-property-sapphire-cut', 'cut', reference_cut)
        return primary_sapphire_color,primary_sapphire_cut

    def _get_primary_topaz_attributes(self, data, reference):
        primary_topaz_color = self._get_attribute(data, 'primary-property-topaz-color', 'color', reference)
        return primary_topaz_color

    def _get_secondary_carnelians(self, data, reference):
        secondary_carnelians = self._get_value(data, 'secondary-carnelians-stone', 'carnelians')
        return secondary_carnelians

    def _get_secondary_chrysoprases(self, data, reference):
        secondary_chrysoprases = self._get_value(data, 'secondary-chrysoprases-stone', 'chrysoprases')
        return secondary_chrysoprases

    def _get_secondary_diamonds(self, data, reference_color, reference_cut):
        secondary_diamonds = self._get_value(data, 'secondary-diamonds-stone', 'diamonds')
        secondary_diamonds_color = self._get_attribute(data, 'secondary-property-diamonds-color', 'color', reference_color)
        secondary_diamonds_cut = self._get_attribute(data, 'secondary-property-diamonds-cut', 'cut', reference_cut)
        return secondary_diamonds, secondary_diamonds_color, secondary_diamonds_cut

    def _get_secondary_emeralds(self, data, reference):
        secondary_emeralds = self._get_value(data, 'secondary-emeralds-stone', 'emeralds')
        return secondary_emeralds

    def _get_secondary_garnets(self, data, reference):
        secondary_garnets = self._get_value(data, 'secondary-garnets-stone', 'garnets')
        secondary_garnets_color = self._get_attribute(data, 'secondary-property-garnets-color', 'color', reference)
        return secondary_garnets, secondary_garnets_color

    def _get_secondary_lapis_lazulis(self, data, reference):
        secondary_lapis_lazulis = self._get_value(data, 'secondary-lapis-lazulis-stone', 'lapis-lazulis')
        return secondary_lapis_lazulis

    def _get_secondary_mother_of_pearl(self, data, reference):
        secondary_mother_of_pearl = self._get_value(data, 'secondary-mother-of-pearl-stone', 'mother-of-pearl')
        secondary_mother_of_pearl_color = self._get_attribute(data, 'secondary-property-mother-of-pearl-color', 'color', reference)
        return secondary_mother_of_pearl, secondary_mother_of_pearl_color

    def _get_secondary_pearls(self, data, reference):
        secondary_pearls = self._get_value(data, 'secondary-pearls-stone', 'pearls')
        return secondary_pearls

    def _get_secondary_peridots(self, data, reference):
        secondary_peridots = self._get_value(data, 'secondary-peridots-stone', 'peridots')
        return secondary_peridots

    def _get_secondary_sapphires(self, data, reference_color, reference_cut):
        secondary_sapphires = self._get_value(data, 'secondary-sapphire-stone', 'sapphire')
        secondary_sapphires_color = self._get_attribute(data, 'secondary-property-sapphire-color', 'color', reference_color)
        secondary_sapphires_cut = self._get_attribute(data, 'secondary-property-sapphire-cut', 'cut', reference_cut)
        return secondary_sapphire, secondary_sapphires_color, secondary_sapphires_cut

    def _get_secondary_spinels(self, data, reference):
        secondary_spinels = self._get_value(data, 'secondary-spinels-stone', 'spinels')
        return secondary_spinels

    def _format_carat_values(data):
        diamond_carats = self._get_carat_attribute(data, 'total-diamond-carats', float, (lambda x: x >= 0 and x <= 8))
        jewel_carats = self._get_carat_attribute(data, 'jewel-weight', float, (lambda x: x >= 0 and x <= 15))
        gold_carats = self._get_carat_attribute(data, 'gold-carats', int, (lambda x: x in (9, 14, 18)))
        return diamond_carats, jewel_carats, gold_carats

    def _get_radio_values(self, data):
        brand_quality = self._get_value(data, 'brand-quality', ('regular', 'high-end'))
        gold_color = self._get_value(data, 'gold-color', ('yellow', 'rose', 'white'))
        return brand_quality, gold_color

    def _get_additional_options(self, data):
        secondary_black_ceramic = self._get_value(data, 'other-black-ceramic-properties', 'black-ceramic')
        secondary_black_lacquer = self._get_value(data, 'other-black-lacquer-properties', 'black-lacquer')
        secondary_rhodium_finish = self._get_value(data, 'other-rhodium-finish-properties', 'rhodium-finish')
        return secondary_black_ceramic, secondary_black_lacquer, secondary_rhodium_finish


