# static method dosent requires any obj creation to use

class ChaiUtils:
    @staticmethod
    def clean_ingredients(text):
        return [item.strip() for item in text.split(",")]
    
raw = " water , milk , ginger , honey "

cleaned = ChaiUtils.clean_ingredients(raw) # direct use
print(cleaned) 