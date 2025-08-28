import random

import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Create server
mcp = FastMCP("Echo Server")

cart_items = {}

class CartItem(BaseModel):
    item_name: str
    quantity: int
    price: float

@mcp.tool()
def add_item_to_cart(cart_item: CartItem) -> str:
    """Add the given item to the cart with the given quantity. Fetch the price of the itemusing web search. 
    If the item is already in the cart, you need to update the quantity.
    """
    print(f"[debug-server] add_item_to_cart({cart_item})")
    if cart_item.item_name in cart_items:
            # Update existing item quantity
            cart_items[cart_item.item_name] = {
                "quantity": cart_items[cart_item.item_name]["quantity"] + cart_item.quantity,
                "price": cart_item.price
            }
    else:
        # Add new item
        cart_items[cart_item.item_name] = {
                "quantity": cart_item.quantity,
                "price": cart_item.price
            }
    return f"Added {cart_item.quantity} {cart_item.item_name} items to the cart. Total items: {cart_items}"

@mcp.tool()
async def get_cart_items() -> str:
    """ Get all the items in the cart"""
    print(f"[debug-server] get_cart_items()")
    if not cart_items:
        return "Cart is empty."
        
    items_list = []
    for item_name, item_data in cart_items.items():
        items_list.append(f"{item_name}: {item_data['quantity']} x ${item_data['price']} = ${item_data['quantity'] * item_data['price']:.2f}")
        
    return "Cart items:\n" + "\n".join(items_list)

@mcp.tool()
async def calcualte_cart_total(cart_items: dict) -> str:
    print(f"[debug-server] calcualte_cart_total()")
    """ Calculate the total value of the cart"""
    total = 0
    for item_name, item_data in cart_items.items():
        total += item_data['quantity'] * item_data['price']
    return f"Total cart value: ${total:.2f}"

# @mcp.tool()
# def get_secret_word() -> str:
#     print("[debug-server] get_secret_word()")
#     return random.choice(["apple", "banana", "cherry"])


# @mcp.tool()
# def get_current_weather(city: str) -> str:
#     print(f"[debug-server] get_current_weather({city})")

#     endpoint = "https://wttr.in"
#     response = requests.get(f"{endpoint}/{city}")
#     return response.text


if __name__ == "__main__":
    mcp.run(transport="sse")