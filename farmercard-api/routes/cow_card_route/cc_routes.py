from typing import List
from fastapi import APIRouter,Depends,HTTPException
from db.cow_card import CowCard


cow_card_router = APIRouter(
    prefix="/cow_card",
    tags=["cow_card"],
    responses={404: {"description": "Not found"}},
)

# In-memory data store for cow cards
cow_cards = []

# Cow Card subroute
@cow_card_router.post("/create_cc", response_model=CowCard)
def create_cow_card(cow_card: CowCard):
    cow_cards.append(cow_card)
    return cow_card

# @cow_card_router.get("/cow_cards/", response_model=List[CowCard])
# def get_all_cow_cards():
#     return cow_cards

# @cow_card_router.get("/cow_cards/{cow_id}", response_model=CowCard)
# def get_cow_card(cow_id: str):
#     for card in cow_cards:
#         if card.identification_info.unique_id == cow_id:
#             return card
#     raise HTTPException(status_code=404, detail="Cow card not found")

# @cow_card_router.put("/cow_cards/{cow_id}", response_model=CowCard)
# def update_cow_card(cow_id: str, updated_card: CowCard):
#     for i, card in enumerate(cow_cards):
#         if card.identification_info.unique_id == cow_id:
#             cow_cards[i] = updated_card
#             return updated_card
#     raise HTTPException(status_code=404, detail="Cow card not found")

# @cow_card_router.delete("/cow_cards/{cow_id}", status_code=204)
# def delete_cow_card(cow_id: str):
#     for i, card in enumerate(cow_cards):
#         if card.identification_info.unique_id == cow_id:
#             del cow_cards[i]
#             return
#     raise HTTPException(status_code=404, detail="Cow card not found")