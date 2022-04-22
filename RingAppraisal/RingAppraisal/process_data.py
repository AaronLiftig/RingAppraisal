class ProcessFormData:
    def __init__(self, constants_data):
        self._get_reference_data(constants_data)

    def process_form_data(self, form_data):
        self._get_form_data(form_data)
        return self._get_input_row_for_model()
        
    def _get_reference_data(self,constants_data):
        #primary stones
        self.primary_reference = list(constants_data['primary_stone'].keys())

        self.diamond_color_reference = constants_data['primary_stone']['diamond']['color']
        self.diamond_cut_reference = constants_data['primary_stone']['diamond']['cut']
        self.diamond_quality_reference = constants_data['primary_stone']['diamond']['quality']
        self.diamond_clarity_reference = constants_data['primary_stone']['diamond']['clarity']
        self.diamond_clarity_reference.remove('LOWER')

        self.sapphire_color_reference = constants_data['primary_stone']['sapphire']['color']

        self.garnet_color_reference = constants_data['primary_stone']['garnet']['color']

        self.pearl_type_reference = constants_data['primary_stone']['pearl']['type']

        self.emerald_cut_reference = constants_data['primary_stone']['emerald']['cut']
        self.emerald_properties_reference = constants_data['primary_stone']['emerald']['properties']

        self.topaz_color_reference = constants_data['primary_stone']['topaz']['color']

        self.quartz_color_reference = constants_data['primary_stone']['quartz']['color']

        #secondary stones
        self.secondary_reference = list(constants_data['secondary_stones'].keys())
        self.secondary_reference = list(map((lambda x: x.replace(' ', '-')), self.secondary_reference))

        self.diamonds_color_reference = constants_data['secondary_stones']['diamonds']['color']
        self.diamonds_cut_reference = constants_data['secondary_stones']['diamonds']['cut']

        self.garnets_color_reference = constants_data['secondary_stones']['garnets']['color']

        self.sapphires_color_reference = constants_data['secondary_stones']['sapphires']['color']
        self.sapphires_cut_reference = constants_data['secondary_stones']['sapphires']['cut']

        self.mother_of_pearl_color_reference = constants_data['secondary_stones']['mother of pearl']['color']

    def _get_form_data(self, form_data):
        self.primary_stone = self._get_primary_stone(form_data, self.primary_reference)
        self.primary_diamond_attributes = self._get_primary_diamond_attributes(form_data, self.diamond_clarity_reference, self.diamond_color_reference,
                                                                                self.diamond_cut_reference, self.diamond_quality_reference)
        self.primary_sapphire_attributes = self._get_primary_sapphire_attributes(form_data, self.sapphire_color_reference)
        self.primary_garnet_attributes = self._get_primary_garnet_attributes(form_data, self.garnet_color_reference)
        self.primary_pearl_attributes = self._get_primary_pearl_attributes(form_data, self.pearl_type_reference)
        self.primary_emerald_attributes = self._get_primary_emerald_attributes(form_data, self.emerald_cut_reference, self.emerald_properties_reference)
        self.primary_topaz_attributes = self._get_primary_topaz_attributes(form_data, self.topaz_color_reference)
        self.primary_quartz_attributes = self._get_primary_quartz_attributes(form_data, self.quartz_color_reference)

        self.secondary_stones = self._get_secondary_stones(form_data)

        self.secondary_diamonds_attributes = self._get_secondary_diamonds(form_data, self.diamonds_color_reference, self.diamonds_cut_reference)
        self.secondary_garnets_attributes = self._get_secondary_garnets(form_data, self.garnets_color_reference)
        self.secondary_sapphires_attributes = self._get_secondary_sapphires(form_data, self.sapphires_color_reference, self.sapphires_cut_reference)
        self.secondary_mother_of_pearl_attributes = self._get_secondary_mother_of_pearl(form_data, self.mother_of_pearl_color_reference)

        self.carat_values = self._format_carat_values(form_data)
        self.radio_values = self._get_radio_values(form_data)
        self.additional_values = self._get_additional_options(form_data)

    def _get_input_row_for_model(self):
        d = {'perimeter-diamonds': 0, 'brilliant-pavé-diamonds': 0} #  zeros for model fields not in form that were excluded for various reasons 

        d['total diamond carats'] = self._clean_attribute(self.carat_values, 0, 0)
        d['jewel_weight'] = self._clean_attribute(self.carat_values, 1, 0)
        d['gold carats'] = self._clean_attribute(self.carat_values, 2, 0)

        gold_color_list = ['color_Black', 'color_Rose', 'color_White', 'color_Yellow']
        d.update(self._get_input_values(self.radio_values, gold_color_list, 1, 'yellow', 
                                   ['black', 'rose', 'white', 'yellow']))

        brand_quality_list = ['brand_Haritidis']
        d.update(self._get_input_values(self.radio_values, brand_quality_list, 0, 'regular',
                                   {'regular':'brand_Haritidis', 'high-end':'brand_Cartier'}))

        additional_values_list = ['black-ceramic', 'black-lacquer', 'rhodium-finish']
        d.update(self._get_input_values(self.additional_values, additional_values_list))

        # primary stone
        d.update(self._get_input_values(self.primary_stone, self.primary_reference))
        
        diamond_clarity_list = ['d','e','f','g']
        diamond_color_list = ['black-diamond','blue-diamond','coffee-diamond','white-diamond']
        diamond_cut_list = ['brilliant-diamond','princess-diamond','troidia-diamond','oval-diamond','baguette-diamond']
        diamond_quality_list = ['si','vs1','vs2','vvs1','vvs2']
        if d['diamond']:
            diamond_d = {}
            d.update(self._get_input_values(self.primary_diamond_attributes, diamond_clarity_list, 0, None, # Updates d because stone is still required
                                       ['D', 'E', 'F', 'G']))
            diamond_d.update(self._get_input_values(self.primary_diamond_attributes, diamond_color_list, 1, None, 
                                       ['black','blue','coffee','white']))
            diamond_d.update(self._get_input_values(self.primary_diamond_attributes, diamond_cut_list, 2, None, 
                                       ['brilliant','princess','troidia','oval','baguette']))
            d.update(self._get_input_values(self.primary_diamond_attributes, diamond_quality_list, 3, None, # Updates d because stone is still required
                                       ['SI','VS1','VS2','VVS1','VVS2']))
            self._remove_base_stone_if_attribute_exists(diamond_d, d, 'diamond')
            d.update(diamond_d)
        else:
            d = self._get_all_zeros(d, diamond_clarity_list + diamond_color_list + diamond_cut_list + diamond_quality_list)

        sapphire_color_list = ['rose-sapphire','blue-sapphire','yellow-sapphire','white-sapphire','pink-sapphire',
                               'green-sapphire','black-sapphire']
        if d['sapphire']:
            sapphire_d = {}
            sapphire_d.update(self._get_input_values(self.primary_sapphire_addributes, sapphire_color_list, None, None, 
                                       ['rose','blue','yellow','white','pink','green','black']))
            self._remove_base_stone_if_attribute_exists(sapphire_d, d, 'sapphire')
            d.update(sapphire_d)
        else:
            d = self._get_all_zeros(d, sapphire_color_list)

        garnet_color_list = ['green-garnet','orange-garnet','tsavorite-garnet']
        if d['garnet']:
            garnet_d = {}
            garnet_d.update(self._get_input_values(self.primary_garnet_attributes, garnet_color_list, None, None, 
                                       ['green', 'orange', 'tsavorite']))
            self._remove_base_stone_if_attribute_exists(garnet_d, d, 'garnet')
            d.update(garnet_d)
        else:
            d = self._get_all_zeros(d, garnet_color_list)
        
        pearl_type_list = ['akoya-pearl','south-sea-pearl','edison-fresh-water-pearl','fresh-water-pearl','edison-pearl']
        if d['pearl']:
            pearl_d = {}
            pearl_d.update(self._get_input_values(self.primary_pearl_attributes, pearl_type_list, None, None, 
                                       ['akoya', 'south sea', 'edison fresh water', 'fresh water', 'edison']))
            self._remove_base_stone_if_attribute_exists(pearl_d, d, 'pearl')
            d.update(pearl_d)
        else:
            d = self._get_all_zeros(d, pearl_type_list)

        emerald_cut_list = ['baguette-brilliant-emerald']
        emerald_properties_list = ['recrystallized-emerald']
        if d['emerald']:
            emerald_d = {}
            emerald_d.update(self._get_input_values(self.primary_emerald_attributes, emerald_cut_list, 0, None, 
                                       ['baguette brilliant']))
            emerald_d.update(self._get_input_values(self.primary_emerald_attributes, emerald_properties_list, 1, None, 
                                       ['recrystallized']))
            self._remove_base_stone_if_attribute_exists(emerald_d, d, 'emerald')
            d.update(emerald_d)
        else:
            d = self._get_all_zeros(d, emerald_cut_list + emerald_properties_list)

        topaz_color_list = ['rainforest-topaz','violac-topaz','blazing-red-topaz','paraiba-topaz','aqua-blue-topaz',
                            'baby-pink-topaz','kashmir-blue-topaz', 'blue-topaz','white-topaz','london-blue-topaz',
                            'red-topaz','green-topaz']
        if d['topaz']:
            topaz_d = {}
            topaz_d.update(self._get_input_values(self.primary_topaz_attributes, topaz_color_list, None, None, 
                                       ['rainforest', 'violac', 'blazing red', 'paraiba', 'aqua blue', 'baby pink', 
                                        'kashmir blue', 'blue', 'white', 'london blue', 'red', 'green']))
            self._remove_base_stone_if_attribute_exists(topaz_d, d, 'topaz')
            d.update(topaz_d)
        else:
            d = self._get_all_zeros(d, topaz_color_list)

        quartz_color_list = ['pink-quartz']
        if d['quartz']:
            quartz_d = {}
            quartz_d.update(self._get_input_values(self.primary_quartz_attributes, quartz_color_list, None, None, 
                                       ['pink']))
            self._remove_base_stone_if_attribute_exists(quartz_d, d, 'quartz')
            d.update(quartz_d)
        else:
            d = self._get_all_zeros(d, topaz_color_list)

        # secondary stones
        d.update(self._get_input_values(self.secondary_stones, self.secondary_reference))

        diamonds_color_list = ['white-diamonds', 'coffee-diamonds', 'blue-diamonds', 'black-diamonds']
        diamonds_cut_list = ['brilliant-diamonds', 'baguette-diamonds', 'princess-diamonds', 'troidia-diamonds',
                              'pear-shaped-diamonds', 'triangle-diamonds', 'baguette-brilliant-diamonds', 
                              'marquise-brilliant-diamonds']
        if d['diamonds']:
            diamonds_d = {}
            diamonds_d.update(self._get_input_values(self.secondary_diamonds_attributes, diamonds_color_list, 0, None, 
                                       ['white', 'coffee', 'blue', 'black']))
            diamonds_d.update(self._get_input_values(self.secondary_diamonds_attributes, diamonds_cut_list, 1, None, 
                                       ['brilliant', 'baguette', 'princess', 'troidia', 'pear shaped', 'triangle',
                                       'baguette brilliant', 'marquise brilliant']))
            self._remove_base_stone_if_attribute_exists(diamonds_d, d, 'diamonds')
            d.update(diamonds_d)
        else:
            d = self._get_all_zeros(d, diamonds_color_list + diamonds_cut_list)

        garnets_color_list = ['tsavorite-garnets']
        if d['garnets']:
            garnets_d = {}
            garnets_d.update(self._get_input_values(self.secondary_garnets_attributes, garnets_color_list, None, None, 
                                       ['tsavorite']))
            self._remove_base_stone_if_attribute_exists(garnets_d, d, 'garnets')
            d.update(garnets_d)
        else:
            d = self._get_all_zeros(d, garnets_color_list)

        sapphires_color_list = ['blue-pink-sapphires', 'blue-sapphires', 'green-sapphires', 'pink-sapphires']
        sapphires_cut_list = ['baguette-brilliant-sapphires']
        if d['sapphires']:
            sapphires_d = {}
            sapphires_d.update(self._get_input_values(self.secondary_sapphires_attributes, sapphires_color_list, 0, None, 
                                       ['blue pink', 'blue', 'green', 'pink']))
            sapphires_d.update(self._get_input_values(self.secondary_sapphires_attributes, sapphires_cut_list, 1, None, 
                                       ['baguette brilliant']))
            self._remove_base_stone_if_attribute_exists(sapphires_d, d, 'sapphires')
            d.update(sapphires_d)
        else:
            d = self._get_all_zeros(d, sapphires_color_list + sapphires_cut_list)

        mother_of_pearl_color_list = ['gray-mother-of-pearl']
        if d['mother-of-pearl']:
            mother_of_pearl_d = {}
            mother_of_pearl_d.update(self._get_input_values(self.secondary_mother_of_pearl_attributes, mother_of_pearl_color_list, None, None, 
                                       ['grey']))
            self._remove_base_stone_if_attribute_exists(mother_of_pearl_d, d, 'mother-of-pearl')
            d.update(mother_of_pearl_d)
        else:
            d = self._get_all_zeros(d, mother_of_pearl_color_list)
        return d

    def _create_dict(self, keys, values):
        return dict(zip(keys,values))
            
    def _get_input_values(self, variable, column_list, index=None, default_value=None, conversion_keys=None):
        d = {}
        if conversion_keys:
            if isinstance(conversion_keys, list):
                conversion_dict = self._create_dict(conversion_keys, column_list)
            elif isinstance(conversion_keys, dict):
                conversion_dict = conversion_keys
        else:
            conversion_dict = None

        if isinstance(variable, tuple) and index is None:
            l = []
            for var in variable:
                l.append(self._clean_attribute(var, index=index, default_value=default_value, conversion_dict=conversion_dict))
            for v in column_list:
                if v in l:
                    d[v] = 1
                else:
                    d[v] = 0
        else:
            value = self._clean_attribute(variable, index=index, default_value=default_value, conversion_dict=conversion_dict)
            for v in column_list:
                if v == value:
                    d[v] = 1
                else:
                    d[v] = 0
        return d

    def _get_all_zeros(self, d, columns_list):
        for v in columns_list:
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
        if not index is None:
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

    def _remove_base_stone_if_attribute_exists(self, attribute_d, d, stone_key):
        if any(attribute_d.values()):
            d[stone_key] = 0
        return d


    def _get_primary_stone(self, data, reference):
        primary_stone = self._get_stone_data(data, 'primary-stone', reference, 'none')
        return primary_stone

    def _get_primary_diamond_attributes(self, data, reference_clarity, reference_color, reference_cut, reference_quality):
        primary_diamond_clairy = self._get_stone_data(data, 'primary-property-diamond-clarity', reference_clarity, 'clarity')
        primary_diamond_color = self._get_stone_data(data, 'primary-property-diamond-color', reference_color, 'color')
        primary_diamond_cut = self._get_stone_data(data, 'primary-property-diamond-cut', reference_cut, 'cut')
        primary_diamond_quality = self._get_stone_data(data, 'primary-property-diamond-quality', reference_quality, 'quality')
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

    def _get_secondary_stones(self, data):
        secondary_carnelians = self._get_stone_data(data, 'secondary-carnelians-stone', 'carnelians')
        secondary_chrysoprases = self._get_stone_data(data, 'secondary-chrysoprases-stone', 'chrysoprases')
        secondary_diamonds = self._get_stone_data(data, 'secondary-diamonds-stone', 'diamonds')
        secondary_emeralds = self._get_stone_data(data, 'secondary-emeralds-stone', 'emeralds')
        secondary_garnets = self._get_stone_data(data, 'secondary-garnets-stone', 'garnets')
        secondary_lapis_lazulis = self._get_stone_data(data, 'secondary-lapis-lazulis-stone', 'lapis-lazulis')
        secondary_mother_of_pearl = self._get_stone_data(data, 'secondary-mother-of-pearl-stone', 'mother-of-pearl')
        secondary_pearls = self._get_stone_data(data, 'secondary-pearls-stone', 'pearls')
        secondary_peridots = self._get_stone_data(data, 'secondary-peridots-stone', 'peridots')
        secondary_sapphires = self._get_stone_data(data, 'secondary-sapphires-stone', 'sapphires')
        secondary_spinels = self._get_stone_data(data, 'secondary-spinels-stone', 'spinels')
        return (secondary_carnelians, secondary_chrysoprases, secondary_diamonds, secondary_emeralds, secondary_garnets,
               secondary_lapis_lazulis, secondary_mother_of_pearl, secondary_pearls, secondary_peridots, secondary_sapphires,
               secondary_spinels)

    def _get_secondary_diamonds(self, data, reference_color, reference_cut):
        secondary_diamonds_color = self._get_stone_data(data, 'secondary-property-diamonds-color', reference_color, 'color')
        secondary_diamonds_cut = self._get_stone_data(data, 'secondary-property-diamonds-cut', reference_cut, 'cut')
        return secondary_diamonds_color, secondary_diamonds_cut

    def _get_secondary_garnets(self, data, reference):
        secondary_garnets_color = self._get_stone_data(data, 'secondary-property-garnets-color', reference, 'color')
        return secondary_garnets_color

    def _get_secondary_mother_of_pearl(self, data, reference):
        secondary_mother_of_pearl_color = self._get_stone_data(data, 'secondary-property-mother-of-pearl-color', reference, 'color')
        return secondary_mother_of_pearl_color

    def _get_secondary_sapphires(self, data, reference_color, reference_cut):
        secondary_sapphires_color = self._get_stone_data(data, 'secondary-property-sapphires-color', reference_color, 'color')
        secondary_sapphires_cut = self._get_stone_data(data, 'secondary-property-sapphires-cut', reference_cut, 'cut')
        return secondary_sapphires_color, secondary_sapphires_cut

    def _format_carat_values(self, data):
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


