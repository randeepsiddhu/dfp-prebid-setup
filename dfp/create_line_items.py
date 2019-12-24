
from googleads import ad_manager

from dfp.client import get_client

def create_line_items(line_items):
  """
  Creates line items in DFP.

  Args:
    line_items (arr): an array of objects, each a line item configuration
  Returns:
    an array: an array of created line item IDs
  """
  dfp_client = get_client()
  line_item_service = dfp_client.GetService('LineItemService', version='v201911')
  line_items = line_item_service.createLineItems(line_items)

  # Return IDs of created line items.
  created_line_item_ids = []
  for line_item in line_items:
    created_line_item_ids.append(line_item['id'])
  return created_line_item_ids


def create_line_item_config(name, order_id, placement_ids, ad_unit_ids, cpm_micro_amount, sizes, key_gen_obj,
                            lineitem_type='PRICE_PRIORITY',currency_code='USD', same_adv_exception=False, device_categories=None,
                            device_capabilities = None,roadblock_type = 'ONE_OR_MORE'):
  """
  Creates a line item config object.

  Args:
    name (str): the name of the line item
    order_id (int): the ID of the order in DFP
    placement_ids (arr): an array of DFP placement IDs to target
    ad_unit_ids (arr): an array of DFP ad unit IDs to target
    cpm_micro_amount (int): the currency value (in micro amounts) of the
      line item
    sizes (arr): an array of objects, each containing 'width' and 'height'
      keys, to set the creative sizes this line item will serve
    key_gen_obj (obj): targeting key gen object
    lineitem_type (str): the type of line item('PRICE_PRIORTY', 'HOUSE' or 'NETWORK')
    currency_code (str): the currency code (e.g. 'USD' or 'EUR')
    same_adv_exception (bool) : https://developers.google.com/ad-manager/api/reference/v201911/LineItemService.LineItem.html#disablesameadvertisercompetitiveexclusion
    roadblock_type (str) : https://developers.google.com/ad-manager/api/reference/v201911/LineItemService.LineItem.html#roadblockingtype
 
  Returns:
    an object: the line item config
  """

  # Set up sizes.
  creative_placeholders = []

  for size in sizes:
    creative_placeholders.append({
      'size': size
    })

  top_set = key_gen_obj.get_dfp_targeting()

  # https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemService.LineItem
  line_item_config = {
    'name': name,
    'orderId': order_id,
    # https://developers.google.com/doubleclick-publishers/docs/reference/v201802/LineItemService.Targeting
    'targeting': {
      'inventoryTargeting': {},
      'customTargeting': top_set,
    },
    'startDateTimeType': 'IMMEDIATELY',
    'unlimitedEndDateTime': True,
    'lineItemType': lineitem_type,
    'costType': 'CPM',
    'costPerUnit': {
      'currencyCode': currency_code,
      'microAmount': cpm_micro_amount
    },
     'valueCostPerUnit':{
      'currencyCode': currency_code,
      'microAmount': cpm_micro_amount
    },
    'roadblockingType': roadblock_type,
    'creativeRotationType': 'EVEN',
    'primaryGoal': {
      'goalType': 'NONE'
    },
    'creativePlaceholders': creative_placeholders,
    'disableSameAdvertiserCompetitiveExclusion': same_adv_exception
  }

  #for network and house line-items, set goal type and units
  if lineitem_type in ('NETWORK','HOUSE'):
    line_item_config['primaryGoal']['goalType'] = 'DAILY'
    line_item_config['primaryGoal']['units'] = 100

  if device_categories != None and len(device_categories) > 0:
      dev_cat_targeting = []
      for dc in device_categories:
          dev_cat_targeting.append({'id': str(dc)})

      line_item_config['targeting']['technologyTargeting'] = {'deviceCategoryTargeting': {'targetedDeviceCategories': dev_cat_targeting}}

  #device capability targetring
  if device_capabilities != None and len(device_capabilities) > 0:
      dev_cap_targeting = []
      for dc in device_capabilities:
          dev_cap_targeting.append({'id': str(dc)})

      line_item_config['targeting']['technologyTargeting'] = {'deviceCapabilityTargeting': {'targetedDeviceCapabilities': dev_cap_targeting}}

  if placement_ids is not None:
    line_item_config['targeting']['inventoryTargeting']['targetedPlacementIds'] = placement_ids

  if ad_unit_ids is not None:
    line_item_config['targeting']['inventoryTargeting']['targetedAdUnits'] = [{'adUnitId': id} for id in ad_unit_ids]

  return line_item_config
