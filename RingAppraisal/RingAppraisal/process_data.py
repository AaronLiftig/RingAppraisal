class ProcessFormData:
    def process_form_data(self, form_data, constants_data):
        self._get_reference_data(constants_data)

        self._get_form_data(form_data)

        return self._get_input_row()
        
    def _get_reference_data(self,constants_data):
        self.primary_reference = list(constants_data.keys())

        self.diamond_color_reference = constants_data['diamond']['color']
        self.diamond_cut_reference = constants_data['diamond']['cut']
        self.diamond_quality_reference = constants_data['diamond']['quality']
        self.diamond_clarity_reference = constants_data['diamond']['clarity'].remove('LOWER')

        self.sapphire_color_reference = constants_data['sapphire']['color']

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

    def _get_form_data(self, form_data):
        self.primary_stone = self._get_primary_stone(form_data, self.primary_reference)
        self.primary_diamond_addributes = self._get_primary_diamond_attributes(form_data, self.diamond_clarity_reference, self.diamond_color_reference,
                                                                                self.diamond_cut_reference, self.diamond_quality_reference)
        self.primary_sapphire_attributes = self._get_primary_sapphire_attributes(form_data, self.sapphire_color_reference)
        self.primary_garnet_attributes = self._get_primary_garnet_attributes(form_data, self.garnet_color_reference)
        self.primary_pearl_attributes = self._get_primary_pearl_attributes(form_data, self.pearl_type_reference)
        self.primary_emerald_attributes = self._get_primary_emerald_attributes(form_data, self.emerald_cut_reference, self.emerald_properties_reference)
        self.primary_topaz_attributes = self._get_primary_topaz_attributes(form_data, self.topaz_color_reference)
        self.primary_quartz_attributes = self._get_primary_quartz_attributes(form_data, self.quartz_color_reference)
        self.secondary_diamonds_attributes = self._get_secondary_diamonds(form_data, self.diamonds_color_reference, self.diamonds_cut_reference)
        self.secondary_garnets_attributes = self._get_secondary_garnets(form_data, self.garnets_color_reference)
        self.secondary_sapphires_attributes = self._get_secondary_sapphires(form_data, self.sapphires_color_reference, self.sapphires_cut_reference)
        self.secondary_mother_of_pearl_attributes = self._get_secondary_mother_of_pearl(form_data, self.mother_of_pearl_color_reference)
        self.carat_values = self._format_carat_values()
        self.radio_values = self._get_radio_values()
        self.additional_values = self._get_additional_options()

    def _get_input_row(self):
        d = {}

        d['total diamond carats'] = self._clean_attribute(self.carat_values, 0, 0)
        d['gold carats'] = self._clean_attribute(self.carat_values, 2, 0)
        d['jewel_weight'] = self._clean_attribute(self.carat_values, 1, 0)

        # gold color
        d = self._get_input_values(d, self.radio_values, ['color_Black', 'color_Rose', 'color_White', 'color_Yellow'], 1, 'yellow', 
                                   {'black':'color_Black', 'rose':'color_Rose', 'white':'color_White', 'yellow':'color_Yellow'})

        # brand quality
        d = self._get_input_values(d, self.radio_values, ['brand_Haritidis'], 0, 'regular',
                                   {'regular':'brand_Haritidis', 'high-end':'brand_Cartier'})

        # primary stone
        d = self._get_input_values(d, self.primary_stone, self.primary_reference)

        if d['diamond']:
            diamond_clarity_list = ['d','e','f','g']
            d = self._get_input_values(d, self.primary_diamond_attributes, diamond_clarity_list, 0, None, 
                                       ['D', 'E', 'F', 'G'])
            diamond_color_list = ['black-diamond','blue-diamond','coffee-diamond','white-diamond']
            d = self._get_input_values(d, self.primary_diamond_attributes, diamond_color_list, 1, None, 
                                       ['black','blue','coffee','white'])
            diamond_cut_list = ['brilliant-diamond','princess-diamond','troidia-diamond','oval-diamond','baguette-diamond']
            d = self._get_input_values(d, self.primary_diamond_attributes, diamond_cut_list, 2, None, 
                                       ['brilliant','princess','troidia','oval','baguette'])
            diamond_quality_list = ['si','vs1','vs2','vvs1','vvs2']
            d = self._get_input_values(d, self.primary_diamond_attributes, diamond_quality_list, 3, None, 
                                       ['SI','VS1','VS2','VVS1','VVS2'])
        else:
            d = self._get_all_zeros(d, diamond_clarity_list + diamond_color_list + diamond_cut_list + diamond_quality_list)

        if d['sapphire']:
            sapphire_color_list = ['rose-sapphire','blue-sapphire','yellow-sapphire','white-sapphire','pink-sapphire','green-sapphire','black-sapphire']
            d = self._get_input_values(d, self.primary_sapphire_addributes, sapphire_color_list, None, None, 
                                       ['rose','blue','yellow','white','pink','green','black'])
        else:
            d = self._get_all_zeros(d, sapphire_color_list)

        if d['garnet']:
            garnet_color_list = ['green-garnet','orange-garnet','tsavorite-garnet']
            d = self._get_input_values(d, self.primary_garnet_attributes, garnet_color_list, None, None, 
                                       ['green', 'orange', 'tsavorite'])
        else:
            d = self._get_all_zeros(d, garnet_color_list)

        if d['pearl']:
            pearl_type_list = ['akoya-pearl','south-sea-pearl','edison-fresh-water-pearl','fresh-water-pearl','edison-pearl']
            d = self._get_input_values(d, self.primary_pearl_attributes, pearl_type_list, None, None, 
                                       ['akoya', 'south-sea', 'edison-fresh-water', 'fresh-water', 'edison'])
        else:
            d = self._get_all_zeros(d, pearl_type_list)

        if d['emerald']:
            emerald_cut_list = ['baguette-brilliant-emerald']
            d = self._get_input_values(d, self.primary_emerald_attributes, emerald_cut_list, 0, None, 
                                       ['baguette-brilliant'])

            emerald_properties_list = ['recrystallized-emerald']
            d = self._get_input_values(d, self.primary_emerald_attributes, emerald_properties_list, 1, None, 
                                       ['recrystallized'])
        else:
            d = self._get_all_zeros(d, emerald_cut_list + emerald_properties_list)

        if d['topaz']:
            topaz_color_list = ['rainforest-topaz','violac-topaz','blazing-red-topaz','paraiba-topaz','aqua-blue-topaz','baby-pink-topaz','kashmir-blue-topaz',
                                'blue-topaz','white-topaz','london-blue-topaz','red-topaz','green-topaz']
            d = self._get_input_values(d, self.primary_topaz_attributes, topaz_color_list, None, None, 
                                       ['rainforest', 'violac', 'blazing-red', 'paraiba', 'aqua-blue', 'baby-pink', 'kashmir-blue', 'blue', 'white', 'london-blue',
                                        'red', 'green'])
        else:
            d = self._get_all_zeros(d, topaz_color_list)

        '''
        ['brilliant-diamonds']
        ['black-ceramic']
        ['amethyst']
        ['emeralds']
        ['onyx']
        ['black-lacquer']
        ['tsavorite-garnets']        
        ['peridots']
        ['diamonds']
        ['gray-mother-of-pearl']
        ['spinels']
        ['carnelians']
        ['chrysoprases']
        ['lapis-lazulis']
        ['brilliant-pavé-diamonds']
        ['baguette-diamonds']
        ['princess-diamonds']
        ['troidia-diamonds']
        ['rhodium-finish']
        ['pear-shaped-diamonds']
        ['amazonite']
        ['coral']
        ['tanzanite']
        ['morganite']
        ['ruby']
        ['citrine']
        ['qendrad']
        ['triangle-diamonds']
        ['spinel']
        ['blue-pink-sapphires']
        ['blue-sapphires']
        ['white-diamonds']
        ['opal']
        ['aquamarine']
        ['sapphires']
        ['baguette-brilliant-diamonds']
        ['marquise-brilliant-diamonds']
        ['rodolite']
        ['coffee-diamonds']
        ['baguette-brilliant-sapphires']
        ['black-diamonds']
        ['pearls']
        ['blue-diamonds']
        ['green-sapphires']
        ['pink-sapphires']
        ['zoisite']
        ['pink-quartz']
        ['quartz']
        ['tourmaline']
        ['mother-of-pearl']
        '''

    def _create_dict(self, keys, values):
        return dict(zip(keys,values))
            
    def _get_input_values(self, d, variable, column_list, index=None, default_value=None, conversion_keys=None):
        if conversion_keys:
            conversion_dict = self._create_dict(conversion_keys, column_list)
        else:
            conversion_dict = None

        value = self._clean_attribute(variable, index=index, default_value=default_value, conversion_dict=conversion_dict)
        for v in column_list:
            if v == value:
                d[v] = 1
            else:
                d[v] = 0
        return d

    def _get_all_zeros(self, d, columns_list):
        for v in column_list:
            d[v] = 0
        return d

    def _get_stone_data(self, data, id, reference, default_name=None):
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

    def _clean_attribute(self, variable, index=None, default_value=None, conversion_dict=None):
        if isinstance(variable, tuple) and not index is None:
            value = variable[index]
        else:
            value = variable

        if not value is None:
            if not conversion_dict is None:
                return conversion_dict[value]
            else:
                return value
        else:
            if not default_value is None:
                if not conversion_dict is None:
                    return conversion_dict[default_value]
                else:
                    return default_value
            else:
                return 0

    def _get_primary_stone(self, data, reference):
        primary_stone = self._get_stone_data(data, 'primary-stone', reference, 'none')
        return primary_stone

    def _get_primary_diamond_attributes(self, data, reference_clarity, reference_color, reference_cut, reference_quality):
        primary_diamond_clairy = self._get_stone_data(data, 'primary-property-diamond-clarity', reference_clarity, 'clarity')
        primary_diamond_color = self._get_stone_data(data, 'primary-property-diamond-color', reference_color, 'color')
        primary_diamond_cut = self._get_stone_data(data, 'primary-property-diamond-cut', reference_cut, 'cut')
        primary_diamond_quality = self._get_stone_data(data, 'primary-property-diamond-quality', reference_quality, 'quality')

        if primary_diamond_clairy:
            primary_diamond_clairy = map((lambda x: x.lower()), primary_diamond_clairy)
        if primary_diamond_quality:
            primary_diamond_quality = map((lambda x: x.lower()), primary_diamond_quality)
        return primary_diamond_clairy, primary_diamond_color, primary_diamond_cut, primary_diamond_quality

    def _get_primary_emerald_attributes(self, data, reference_cut, reference_properties):
        primary_emerald_cut = self._get_stone_data(data, 'primary-property-emerald-cut', reference_cut, 'cut')
        primary_emerald_properties = self._get_stone_data(data, 'primary-property-emerald-properties', reference_properties, 'properties')
        return primary_emerald_cut, primary_emerald_properties

    def _get_primary_garnet_attributes(self, data, reference):
        primary_garnet_color = self._get_stone_data(data, 'primary-property-garnet-color', reference, 'color')
        return primary_garnet_color

    def _get_primary_pearl_attributes(self, data, reference):
        primary_pearl_type = self._get_stone_data(data, 'primary-property-pearl-type', reference, 'type')
        return primary_pearl_type

    def _get_primary_quartz_attributes(self, data, reference):
        primary_quartz_color = self._get_stone_data(data, 'primary-property-quartz-color', reference, 'color')
        return primary_quartz_color

    def _get_primary_sapphire_attributes(self, data, reference):
        primary_sapphire_color = self._get_stone_data(data, 'primary-property-sapphire-color', reference, 'color')
        return primary_sapphire_color

    def _get_primary_topaz_attributes(self, data, reference):
        primary_topaz_color = self._get_stone_data(data, 'primary-property-topaz-color', reference, 'color')
        return primary_topaz_color

    def _get_secondary_carnelians(self, data, reference):
        secondary_carnelians = self._get_stone_data(data, 'secondary-carnelians-stone', 'carnelians')
        return secondary_carnelians

    def _get_secondary_chrysoprases(self, data, reference):
        secondary_chrysoprases = self._get_stone_data(data, 'secondary-chrysoprases-stone', 'chrysoprases')
        return secondary_chrysoprases

    def _get_secondary_diamonds(self, data, reference_color, reference_cut):
        secondary_diamonds = self._get_stone_data(data, 'secondary-diamonds-stone', 'diamonds')
        secondary_diamonds_color = self._get_stone_data(data, 'secondary-property-diamonds-color', reference_color, 'color')
        secondary_diamonds_cut = self._get_stone_data(data, 'secondary-property-diamonds-cut', reference_cut, 'cut')
        return secondary_diamonds, secondary_diamonds_color, secondary_diamonds_cut

    def _get_secondary_emeralds(self, data, reference):
        secondary_emeralds = self._get_stone_data(data, 'secondary-emeralds-stone', 'emeralds')
        return secondary_emeralds

    def _get_secondary_garnets(self, data, reference):
        secondary_garnets = self._get_stone_data(data, 'secondary-garnets-stone', 'garnets')
        secondary_garnets_color = self._get_stone_data(data, 'secondary-property-garnets-color', reference, 'color')
        return secondary_garnets, secondary_garnets_color

    def _get_secondary_lapis_lazulis(self, data, reference):
        secondary_lapis_lazulis = self._get_stone_data(data, 'secondary-lapis-lazulis-stone', 'lapis-lazulis')
        return secondary_lapis_lazulis

    def _get_secondary_mother_of_pearl(self, data, reference):
        secondary_mother_of_pearl = self._get_stone_data(data, 'secondary-mother-of-pearl-stone', 'mother-of-pearl')
        secondary_mother_of_pearl_color = self._get_stone_data(data, 'secondary-property-mother-of-pearl-color', reference, 'color')
        return secondary_mother_of_pearl, secondary_mother_of_pearl_color

    def _get_secondary_pearls(self, data, reference):
        secondary_pearls = self._get_stone_data(data, 'secondary-pearls-stone', 'pearls')
        return secondary_pearls

    def _get_secondary_peridots(self, data, reference):
        secondary_peridots = self._get_stone_data(data, 'secondary-peridots-stone', 'peridots')
        return secondary_peridots

    def _get_secondary_sapphires(self, data, reference_color, reference_cut):
        secondary_sapphires = self._get_stone_data(data, 'secondary-sapphire-stone', 'sapphire')
        secondary_sapphires_color = self._get_stone_data(data, 'secondary-property-sapphire-color', reference_color, 'color')
        secondary_sapphires_cut = self._get_stone_data(data, 'secondary-property-sapphire-cut', reference_cut, 'cut')
        return secondary_sapphire, secondary_sapphires_color, secondary_sapphires_cut

    def _get_secondary_spinels(self, data, reference):
        secondary_spinels = self._get_stone_data(data, 'secondary-spinels-stone', 'spinels')
        return secondary_spinels

    def _format_carat_values(data):
        diamond_carats = self._get_carat_attribute(data, 'total-diamond-carats', float, (lambda x: x >= 0 and x <= 8))
        jewel_carats = self._get_carat_attribute(data, 'jewel-weight', float, (lambda x: x >= 0 and x <= 15))
        gold_carats = self._get_carat_attribute(data, 'gold-carats', int, (lambda x: x in (9, 14, 18)))
        return diamond_carats, jewel_carats, gold_carats

    def _get_radio_values(self, data):
        brand_quality = self._get_stone_data(data, 'brand-quality', ('regular', 'high-end'))
        gold_color = self._get_stone_data(data, 'gold-color', ('yellow', 'rose', 'white', 'black'))
        return brand_quality, gold_color

    def _get_additional_options(self, data):
        secondary_black_ceramic = self._get_stone_data(data, 'other-black-ceramic-properties', 'black-ceramic')
        secondary_black_lacquer = self._get_stone_data(data, 'other-black-lacquer-properties', 'black-lacquer')
        secondary_rhodium_finish = self._get_stone_data(data, 'other-rhodium-finish-properties', 'rhodium-finish')
        return secondary_black_ceramic, secondary_black_lacquer, secondary_rhodium_finish


