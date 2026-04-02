import json
import os
import traceback
from webui import webui

from backend.engine import cari_resep, load_database

# Basic state memory
APP_STATE = {
    "current_ingredients": [],
    "recent_searches": [],
    "current_results": [],
    "selected_recipe_id": None
}

db = load_database()

def search_recipes(e):
    try:
        data_str = e.get_string()
    except Exception as ex:
        e.return_string(json.dumps({"success": False, "error": str(ex)}))
        return
        
    try:
        ingredients = json.loads(data_str)
    except Exception as exc:
        print(f"Error parsing JSON from UI: {exc}, raw data: {data_str}")
        e.return_string(json.dumps({"success": False, "error": str(exc)}))
        return
        
    print(f"[Backend] Searching for: {ingredients}")
    
    if ingredients and ingredients not in APP_STATE["recent_searches"]:
        APP_STATE["recent_searches"].insert(0, ingredients)
        if len(APP_STATE["recent_searches"]) > 3:
            APP_STATE["recent_searches"].pop()
            
    try:
        APP_STATE["current_ingredients"] = ingredients
        results = cari_resep(ingredients)
        APP_STATE["current_results"] = results
        print(f"[Backend] Found {len(results)} recipes!")
        e.return_string(json.dumps({"success": True}))
    except Exception as exc:
        print(f"[Backend] Search Error: {exc}")
        traceback.print_exc()
        e.return_string(json.dumps({"success": False, "error": str(exc)}))

def get_recent_searches(e):
    e.return_string(json.dumps(APP_STATE["recent_searches"]))

def clear_recent_searches(e):
    APP_STATE["recent_searches"] = []
    e.return_string(json.dumps({"success": True}))

def get_search_results(e):
    e.return_string(json.dumps({
        "ingredients": APP_STATE["current_ingredients"],
        "results": APP_STATE["current_results"]
    }))

def view_recipe_details(e):
    try:
        data_str = e.get_string()
    except Exception as ex:
        e.return_string(json.dumps({"success": False, "error": str(ex)}))
        return
        
    try:
        recipe_id = int(data_str)
        print(f"[Backend] Selected recipe: {recipe_id}")
        APP_STATE["selected_recipe_id"] = recipe_id
        e.return_string(json.dumps({"success": True}))
    except Exception as exc:
        print(f"[Backend] Selected recipe Error: {exc}")
        e.return_string(json.dumps({"success": False}))

def get_recipe_details(e):
    recipe_id = APP_STATE.get("selected_recipe_id")
    if recipe_id is None:
        e.return_string(json.dumps({"error": "No recipe selected"}))
        return
    
    match_info = {}
    for res in APP_STATE["current_results"]:
        if res["id"] == recipe_id:
            match_info = {
                "match_percentage": res.get("match_percentage", 0),
                "available_ingredients": res.get("available_ingredients", []),
                "missing_ingredients": res.get("missing_ingredients", [])
            }
            break

    for r in db:
        if r["id"] == recipe_id:
            r_copy = r.copy()
            r_copy.update(match_info)
            e.return_string(json.dumps(r_copy))
            return
            
    e.return_string(json.dumps({"error": "Recipe not found"}))

if __name__ == "__main__":
    window = webui.window()
    
    window.bind("search_recipes", search_recipes)
    window.bind("get_recent_searches", get_recent_searches)
    window.bind("clear_recent_searches", clear_recent_searches)
    window.bind("get_search_results", get_search_results)
    window.bind("view_recipe_details", view_recipe_details)
    window.bind("get_recipe_details", get_recipe_details)
    
    window.set_root_folder("..") # Since we will run this from c:\MobApps or we can just serve C:\MobApps
    
    # We want to serve frontend folder so resources are loaded correctly
    window.set_root_folder("frontend")
    
    # But images are in c:\MobApps\images wait... the user said they are in frontend/images or just images
    # The JSON paths are "images/id-1.jpg". 
    # If the root folder is 'frontend' and the images are in 'frontend/images', this will work perfectly.
    
    window.show("home.html")

    try:
        port = window.get_port()
        print("=" * 45)
        print("  FridgeMate is running!")
        print(f"  Local: http://localhost:{port}/home.html")
        print("=" * 45)
    except Exception:
        print("=" * 45)
        print("  FridgeMate is running!")
        print("  (Browser window should open automatically)")
        print("=" * 45)

    webui.wait()
