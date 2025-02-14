from kucoin_universal_sdk.generate.spot.market.model_get_announcements_req import GetAnnouncementsReqBuilder, GetAnnouncementsReq


def get_new_listings(spot_market_api):
    params = (GetAnnouncementsReqBuilder()
              .set_ann_type(GetAnnouncementsReq.AnnTypeEnum.NEW_LISTINGS)
              .set_current_page(1)
              .set_page_size(1)
              .build())
    return spot_market_api.get_announcements(params)