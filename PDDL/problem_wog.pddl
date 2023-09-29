(define (problem master)

(:domain New_domain_wog)

(:objects 

;Avoiding grounding
  
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


;; distance in meters.

    ( = (distance Bedroom Kitchen) 60)
    ( = (distance Bedroom LivingRoom) 50)
    ( = (distance Bedroom Pantry) 140)
    ( = (distance Bedroom Garden) 170)
    ( = (distance Bedroom Bedroom) 0)
  

    ( = (distance Kitchen Kitchen) 0)
    ( = (distance Kitchen LivingRoom) 100)
    ( = (distance Kitchen Pantry) 80)
    ( = (distance Kitchen Garden) 110)
    ( = (distance Kitchen Bedroom) 60)
  

    ( = (distance LivingRoom Kitchen) 100)
    ( = (distance LivingRoom LivingRoom) 0)
    ( = (distance LivingRoom Pantry) 90)
    ( = (distance LivingRoom Garden) 110)
    ( = (distance LivingRoom Bedroom) 50)


    ( = (distance Pantry Kitchen) 80)
    ( = (distance Pantry LivingRoom) 90)
    ( = (distance Pantry Pantry) 0)
    ( = (distance Pantry Garden) 20)
    ( = (distance Pantry Bedroom) 140)


    ( = (distance Garden Kitchen) 110)
    ( = (distance Garden LivingRoom) 110)
    ( = (distance Garden Pantry) 20)
    ( = (distance Garden Garden) 0)
    ( = (distance Garden Bedroom) 170)
  



( = (total-cost) 0) 

;(not(stuff_at Cooked_Maggie stove Kitchen))
;(sliced Sliced_Mango)
;(stuff_at Cleaned_clothes WashingMachine Pantry)
;(stuff_at remaining_food plate Bedroom)

;(stuff_at Remaining_veggy plate Bedroom)
; (agent_at Pantry)
; (stuff_at Clothes WashingMachine Pantry)
)

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





; Fire extinguisher


