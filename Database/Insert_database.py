from Database.database_connection import Create_connection
from Utils.data_logger import log_info, log_error,log_warning
from Utils.Exception import DatabaseConnectionError

def insert_items():
    conn = Create_connection()

    query_coldDrink = """ INSERT INTO ColdDrinks (ID, Brand_name, Price, Added, Opening_Balance, Closing_Balance, Total_Sale) 
    VALUES 
    ('T20', 'Thums up (200ml)', 20, 0, 0, 0, 0),
    ('T20(250)', 'Thums up (250ml)', 20, 0, 0, 0, 0),
    ('T50', 'Thums up (750ml)', 50, 0, 0, 0, 0),
    ('S20', 'Soda (300ml)', 20, 0, 0, 0, 0),
    ('R125', 'Red Bull (250ml)', 125, 0, 0, 0, 0),
    ('M10', 'Mineral water (500ml)', 10, 0, 0, 0, 0),
    ('M20', 'Mineral water (1000ml)', 20, 0, 0, 0, 0);
    """
    query_snacks = """INSERT INTO Snacks (ID, Brand_name, Price, Added, Opening_Balance, Closing_Balance, Total_Sale) 
    VALUES 
    ('S5', 'Snacks', 5, 0, 0, 0, 0),
    ('S10', 'Snacks', 10, 0, 0, 0, 0),
    ('S20', 'Snacks', 20, 0, 0, 0, 0),
    ('S25', 'Snacks', 25, 0, 0, 0, 0);
    """
    query_liquor = """ INSERT INTO Liquor (ID, Brand_name, Price, Added, Opening_Balance, Closing_Balance, Total_Sale)
      VALUES
('RS180', 'R.Stag (180ml)', 240, 0, 0, 0, 0),
('NO180', 'No.1 (180ml)', 210, 0, 0, 0, 0),
('MP180', 'MagicP (180ml)', 0, 0, 0, 0, 0),
('MF180', 'MagicF (180ml)', 0, 0, 0, 0, 0),
('RP180', 'Rom.P (180ml)', 0, 0, 0, 0, 0),
('Ro180', 'Rom.F (180ml)', 0, 0, 0, 0, 0),
('WM180', 'WMC P (180ml)', 0, 0, 0, 0, 0),
('IB180', 'IB (180ml)', 210, 0, 0, 0, 0),
('DS180', 'DSP(B) (180ml)', 200, 0, 0, 0, 0),
('BP180', 'BP (180ml)', 0, 0, 0, 0, 0),
('OC180', 'O.C (180ml)', 0, 0, 0, 0, 0),
('OB180', 'O.C.Blue (180ml)', 0, 0, 0, 0, 0),
('8P180', '8PM (180ml)', 0, 0, 0, 0, 0),
('RR180', 'R.Rum (180ml)', 170, 0, 0, 0, 0),
('OM180', 'OM (180ml)', 0, 0, 0, 0, 0),
('HY180', 'Hayward (180ml)', 0, 0, 0, 0, 0),
('DC180', 'Doctor (180ml)', 150, 0, 0, 0, 0),
('GG180', 'GoaGin (180ml)', 150, 0, 0, 0, 0),
('RC180', 'RC (180ml)', 240, 0, 0, 0, 0),
('SG180', 'Signature (180ml)', 0, 0, 0, 0, 0),
('GM180', 'G.M.F. (180ml)', 270, 0, 0, 0, 0),
('BA180', 'Bacardi(B) (180ml)', 220, 0, 0, 0, 0),
('B7_180', 'B7 (180ml)', 240, 0, 0, 0, 0),
('OKG180', 'Oksmith(G) (180ml)', 0, 0, 0, 0, 0),
('OKS180', 'Oksmith(S) (180ml)', 0, 0, 0, 0, 0),
('SB180', 'S.Ball(F) (180ml)', 0, 0, 0, 0, 0),
('RSB180', 'R.S.(B) (180ml)', 0, 0, 0, 0, 0),
('RF180', 'R.Ford (180ml)', 0, 0, 0, 0, 0),
('MB180', 'M.B. (180ml)', 0, 0, 0, 0, 0),
('AP180', 'AmericanPride (180ml)', 370, 0, 0, 0, 0),
('BD180', 'BlackDog (180ml)', 0, 0, 0, 0, 0),
('BG180', 'BlackDogGold (180ml)', 0, 0, 0, 0, 0),
('Rk180', 'RockFord (180ml)', 0, 0, 0, 0, 0),
('V69_180', 'Vat69 (180ml)', 0, 0, 0, 0, 0),
('RL180', 'RedLabel (180ml)', 0, 0, 0, 0, 0),
('GL180', 'GreenLabel (180ml)', 0, 0, 0, 0, 0),
('SM180', 'SimronOff (180ml)', 0, 0, 0, 0, 0),
('RG180', 'RoyalGreen (180ml)', 250, 0, 0, 0, 0),
('BW180', 'Black&White (180ml)', 0, 0, 0, 0, 0),
('BB180', 'BlackBakardi(PL) (180ml)', 0, 0, 0, 0, 0),
('100P180', '100Piper (180ml)', 0, 0, 0, 0, 0),
('JD180', 'JackDaniels (180ml)', 0, 0, 0, 0, 0),
('TC180', 'Teachers (180ml)', 0, 0, 0, 0, 0),
('AQ180', 'Antiquity (180ml)', 0, 0, 0, 0, 0),
('RS90', 'RoyalStag (90ml)', 130, 0, 0, 0, 0),
('NO90', 'No.1 (90ml)', 110, 0, 0, 0, 0),
('MP90', 'MagicP (90ml)', 0, 0, 0, 0, 0),
('MF90', 'MagicF (90ml)', 0, 0, 0, 0, 0),
('WM90', 'WMC (90ml)', 0, 0, 0, 0, 0),
('RP90', 'RomanovP (90ml)', 0, 0, 0, 0, 0),
('RF90', 'RomanovF (90ml)', 0, 0, 0, 0, 0),
('IB90', 'IB (90ml)', 110, 0, 0, 0, 0),
('DS90', 'DSP(B) (90ml)', 100, 0, 0, 0, 0),
('OC90', 'O.C (90ml)', 0, 0, 0, 0, 0),
('OM90', 'OM (90ml)', 0, 0, 0, 0, 0),
('8P90', '8PM (90ml)', 0, 0, 0, 0, 0),
('RR90', 'R.Rum (90ml)', 100, 0, 0, 0, 0),
('DC90', 'Doctor (90ml)', 80, 0, 0, 0, 0),
('B7_90', 'B7 (90ml)', 130, 0, 0, 0, 0),
('GG90', 'GoaGin (90ml)', 0, 0, 0, 0, 0),
('RC90', 'RC (90ml)', 0, 0, 0, 0, 0),
('BP90', 'BlendersPride (90ml)', 230, 0, 0, 0, 0),
('SG90', 'Signature (90ml)', 0, 0, 0, 0, 0),
('MB90', 'M.B. (90ml)', 0, 0, 0, 0, 0),
('GM90', 'GrandMasterF (90ml)', 0, 0, 0, 0, 0),
('RB90', 'RoyalStagBarrel (90ml)', 0, 0, 0, 0, 0),
('RG90', 'RoyalGreen (90ml)', 130, 0, 0, 0, 0),
('CB650', 'Carlsberg (650ml)', 0, 0, 0, 0, 0),
('KF650', 'Kingfisher (650ml)', 240, 0, 0, 0, 0),
('KO650', 'Knockout (650ml)', 0, 0, 0, 0, 0),
('TB650', 'Tuborg (650ml)', 240, 0, 0, 0, 0),
('TC650', 'TuborgClassic (650ml)', 0, 0, 0, 0, 0),
('BW650', 'Budweiser (650ml)', 0, 0, 0, 0, 0),
('HY650', 'Haywards2000 (650ml)', 0, 0, 0, 0, 0),
('RC650', 'RC (650ml)', 0, 0, 0, 0, 0),
('XX650', 'XX (650ml)', 0, 0, 0, 0, 0),

('RC500', 'RC (500ml)', 0, 0, 0, 0, 0),
('LP500', 'L.P. (500ml)', 0, 0, 0, 0, 0),
('HY500', 'Haywards2000 (500ml)', 0, 0, 0, 0, 0),
('XX500', 'XX (500ml)', 0, 0, 0, 0, 0),

('SB330', '330ml Strong Beer', 0, 0, 0, 0, 0),
('KF330', 'Kingfisher (330ml)', 0, 0, 0, 0, 0),
('TB330', 'Tuborg (330ml)', 150, 0, 0, 0, 0),

('MB650', '650ml Mild Beer', 0, 0, 0, 0, 0),
('LP650', 'L.P. (650ml)', 0, 0, 0, 0, 0),

('MB500', '500ml Mild Beer', 0, 0, 0, 0, 0),
('KF500', 'Kingfisher (500ml)', 0, 0, 0, 0, 0),
('BW500', 'Budweiser (500ml)', 0, 0, 0, 0, 0),
('CB500', 'Carlsberg (500ml)', 0, 0, 0, 0, 0),
('TB500', 'Tuborg (500ml)', 0, 0, 0, 0, 0); 
"""

    try:
        cursor = conn.cursor()
        cursor.execute(query_coldDrink)
        conn.commit()
        log_info("Items addedd successfully into the database")
    except Exception as e:
        log_error(f"Error occured while intserting the items into the databases {e}")
        print(Exception)

    try:
        cursor = conn.cursor()
        cursor.execute(query_snacks)
        conn.commit()
        log_info("Items addedd successfully into the database")
    except Exception as e:
        log_error(f"Error occured while intserting the items into the databases {e}")
        print(Exception)

    
    try:
        cursor = conn.cursor()
        cursor.execute(query_liquor)
        conn.commit()
        log_info("Items addedd successfully into the database")
    except Exception as e:
        log_error(f"Error occured while intserting the items into the databases {e}")
        print(Exception)

    finally:
        conn.close()