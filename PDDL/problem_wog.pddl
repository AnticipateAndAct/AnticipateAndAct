(define (problem master)

(:domain New_domain_wog)

(:objects 

Fridge Shelf Table - receptacle
          
Apple Sliced_Apple Mango Sliced_Mango - fruit
    
Maggie Cooked_Maggie cereal Cooked_cereal - food
    
Potato Veggie - vegetable
    
wine milk - drink
    
Laptop cup - obj
    
mold cake - tobake
        
)



(:init
   
   ;Initially
    
    (agent_at Bedroom)
   
    (switched_off faucet Kitchen) 
    (switched_off Television Bedroom) 
    (switched_off Morning_Radio Bedroom) 
    (switched_off Light Bedroom) 
    (switched_off Alarm Bedroom) 
    (switched_off Burner Kitchen) 
    (switched_off Oven_switch Kitchen) 
    (switched_off WashingMachine_switch Pantry)
    (switched_off VacuumCleaner livingRoom)
    (switched_off watering_hose Garden)
    (switched_off LawnMower Garden)
    (switched_off Dishwasher_Switch Kitchen)
    (switched_off extinguisher Kitchen)
    (not(open WashingMachine Pantry)) 
    
    (obj_at VacuumCleaner Pantry)
    (obj_at watering_hose Pantry)
    (obj_at gardening_tools Pantry)
    (obj_at LawnMower Pantry)
    (obj_at Television Bedroom)
    (obj_at Faucet Kitchen)
    (obj_at burner Kitchen)
    (obj_at Oven_switch Kitchen)
    (obj_at WashingMachine_switch Pantry)
    (obj_at Dishwasher_Switch Kitchen)
    (obj_at extinguisher Pantry)
    (obj_at Alarm Bedroom)
    (obj_at Morning_Radio Bedroom)
    (obj_at Light Bedroom)
    

    (stuff_at Clothes LaundryBag LivingRoom)
    (stuff_at trash_1 Dustbin_1 Kitchen)
    (stuff_at trash_2 Dustbin_2 Bedroom)
    (stuff_at trash Master_Dustbin Garden)
    (stuff_at Dirtydishes Basin Kitchen)
    (stuff_at DustMop drawer Pantry)
    (stuff_at Laptop Table Bedroom)
    

    (not(open Oven Kitchen))

    ;Stuff at

    (stuff_at Apple Fridge Kitchen)
    (equal Apple Sliced_Apple)
  
    (stuff_at Mango Fridge Kitchen)
    (equal Mango Sliced_Mango)
    
    (stuff_at Maggie Shelf Kitchen)
    (equal Maggie Cooked_Maggie)

    (stuff_at cereal Shelf Kitchen)
    (equal cereal Cooked_cereal)
    
    (stuff_at mold Shelf Kitchen)
    (equal mold cake)
 
    (stuff_at wine Shelf Kitchen)
    (stuff_at milk Fridge Kitchen)

    (stuff_at Veggie Fridge Kitchen) 
    (equal Veggie Veggie)

    (stuff_at Potato Fridge Kitchen) 
    (equal Potato Potato)

    (food_remaining)  


   ;Time taken to move between locations

    ( = (duration_ Bedroom Kitchen) 60)
    ( = (duration_ Bedroom LivingRoom) 50)
    ( = (duration_ Bedroom Pantry) 140)
    ( = (duration_ Bedroom Garden) 170)
    ( = (duration_ Bedroom Bedroom) 0)
  

    ( = (duration_ Kitchen Kitchen) 0)
    ( = (duration_ Kitchen LivingRoom) 100)
    ( = (duration_ Kitchen Pantry) 80)
    ( = (duration_ Kitchen Garden) 110)
    ( = (duration_ Kitchen Bedroom) 60)
  

    ( = (duration_ LivingRoom Kitchen) 100)
    ( = (duration_ LivingRoom LivingRoom) 0)
    ( = (duration_ LivingRoom Pantry) 90)
    ( = (duration_ LivingRoom Garden) 110)
    ( = (duration_ LivingRoom Bedroom) 50)


    ( = (duration_ Pantry Kitchen) 80)
    ( = (duration_ Pantry LivingRoom) 90)
    ( = (duration_ Pantry Pantry) 0)
    ( = (duration_ Pantry Garden) 20)
    ( = (duration_ Pantry Bedroom) 140)


    ( = (duration_ Garden Kitchen) 110)
    ( = (duration_ Garden LivingRoom) 110)
    ( = (duration_ Garden Pantry) 20)
    ( = (duration_ Garden Garden) 0)
    ( = (duration_ Garden Bedroom) 170)
  



( = (total-cost) 0) 

;(not(stuff_at Cooked_Maggie stove Kitchen))
;(sliced Sliced_Mango)
;(stuff_at Cleaned_clothes WashingMachine Pantry)
;(stuff_at remaining_food plate Bedroom)
;(stuff_at Remaining_veggy plate Bedroom)
;(agent_at Pantry)
;(stuff_at Clothes WashingMachine Pantry)

)

;Comment the goal states that you dont need.
(:goal (and

   (Awake)

   (fruit_served Sliced_Apple Bedroom)
   (food_served Cooked_cereal Bedroom)
   (veggy_served Veggie Bedroom)
   (served_drink Milk Bedroom)
   (baked_served cake Bedroom)

   (cleaned_food Remaining_food Bedroom)
   (cleaned_food Remaining_fruit Bedroom)
   (cleaned_food Remaining_veggy Bedroom)
   (cleaned_food Remaining_baked Bedroom)

   (CleanedHouse)
   (dusted sofa livingRoom)
   (laundrydone)

   (watering_plants)
   (cutting_done)

   (Trash_cleared)
   (movie_started)

)
)

(:metric minimize (total-cost))


)


