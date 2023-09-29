(define (domain New_domain_wog)


(:requirements :strips :negative-preconditions :typing :disjunctive-preconditions :action-costs)


(:types location obj receptacle - object ; supertype
        fruit food vegetable tobake drink - obj)


(:constants
    
    LivingRoom Kitchen Garden Pantry Bedroom - location

    Alarm Light Morning_Radio - obj 

  
    Faucet VacuumCleaner watering_hose Burner Oven_switch WashingMachine_switch water Remaining_food Remaining_fruit Remaining_baked Remaining_veggy Dirtydishes Dishwasher_Switch - obj 

    Television trash_1 trash_2 trash cleaned_dishes - obj 

    Clothes Cleaned_clothes gardening_tools LawnMower Ironed_clothes folded_clothes DustMop Sofa Window extinguisher - obj

    Stove Basin CounterTop Dustbin_1 Dustbin_2 Master_Dustbin Oven WashingMachine plate glass Dryer LaundryBag IroningBoard Dishwasher Closet drawer - receptacle 

)

(:predicates
    
 (Awake)
    
 (agent_at ?l - location)
 (receptacle_at ?r - receptacle ?l - location)
 (obj_at ?o - obj ?l - location)
 (stuff_at ?o - obj ?r - receptacle ?l - location)
 (switched_on ?o - obj ?l - location)
 (switched_off ?o - obj ?l - location)

 (In_hand ?o - obj)

;avoiding grounding
 
 (cleaned ?o - obj)
 (sliced ?o - obj)
 (cooked ?o - obj)
 (fruit_served ?o - fruit  ?l - location)
 (food_served ?o - food ?l - location)
 (baked_served ?o - tobake ?l - location)
 (equal ?o1 ?o2 - obj)
 (baked ?o - tobake)
 (served_drink ?o1 - drink ?l - location)
 (food_remaining)
 (veggy_served ?o1 - vegetable ?l - location)
 
 (open ?r - receptacle ?l - location)
 (washed ?o - obj) 
 (CleanedHouse)
 (dropped ?o1 - obj ?r - receptacle ?l - location)


 (cleaned_food ?o - obj ?l - location)
 (Dried ?o - obj)
 (Ironedclothes)
 (clothes_folded)
 (laundrydone)
 (dusted ?o - obj ?l - location)

 ;gardening
 (watering_plants)
 (cutting_done)
 (Trash_cleared)
 (dishes_cleaned)

 (dim_the_lights ?l - location)
 (movie_started)
 (FireExtinguished)
)

(:functions 
    (distance ?l1 ?l2 - location)
    (total-cost)
)

(:action Wake_up ;working
 :parameters()
 :precondition (and
                   (agent_at Bedroom)
                   (switched_on Alarm Bedroom)
                   (switched_on Morning_Radio Bedroom)
                   (switched_on Light Bedroom)
                   (not(Awake))
               )
 :effect(Awake) 
)

(:action move_agent ;working
 :parameters (?l1 ?l2 - location)
 :precondition (and(agent_at ?l1)
                   )
 :effect(and(not(agent_at ?l1))
            (agent_at ?l2)
            (increase (total-cost)(distance ?l1 ?l2))
        )
)



(:action Switch_on ;working
 :parameters(?o - obj ?l - location)
 :precondition(and(switched_off ?o ?l)
                  (agent_at ?l)
                  (obj_at ?o ?l)
                  (not(switched_on ?o ?l)))
 :effect(and(not(switched_off ?o ?l))
                (switched_on ?o ?l)
                (increase (total-cost) 1))
)


(:action Switch_off ;working
 :parameters(?o - obj ?l - location)
 :precondition(and(switched_on ?o ?l)
                  (agent_at ?l)
                  (obj_at ?o ?l)
                  (not(switched_off ?o ?l)))
 :effect(and(switched_off ?o ?l)
            (not(switched_on ?o ?l))
        )
)

(:action PickUp ;food
 :parameters(?o - obj ?r - receptacle ?l - location)
 :precondition(and(agent_at ?l)
                  (stuff_at ?o ?r ?l)
                  (not(In_hand ?o)))
 :effect(and(In_hand ?o)
            (not(stuff_at ?o ?r ?l))
            (increase (total-cost) 5)
        )
)



(:action PutDown ;food
 :parameters (?o - obj ?r -  receptacle ?l - location)
 :precondition (and(agent_at ?l)
                   (In_hand ?o)
                )
 :effect (and(not(In_hand ?o))
             (stuff_at ?o ?r ?l)
             (increase (total-cost) 5))  
) 


(:action PickUp_Object ;working
 :parameters(?o - obj ?l - location)
 :precondition(and(agent_at ?l)
                  (obj_at ?o ?l)
                  
                  (not(In_hand ?o)))
 :effect(and(In_hand ?o)
            (not(obj_at ?o ?l))
            (increase (total-cost) 5)
        )
)

(:action PutDown_Object ;working
 :parameters (?o - obj ?l - location)
 :precondition (and(agent_at ?l)
                   (In_hand ?o)
                   
                )
 :effect (and(not(In_hand ?o))
             (obj_at ?o ?l)
             (increase (total-cost) 5))  
) 

(:action Open      ;working              
 :parameters (?r - receptacle ?l - location)
 :precondition(and(agent_at ?l)
                  (receptacle_at ?r ?l)
                  (not(open ?r ?l)))
 :effect(and(open ?r ?l)
            (increase (total-cost) 2)
        ) 
)


(:action dusting_with_dustmop ;working
 :parameters(?o - obj ?l - location)
 :precondition(and(In_hand DustMop)  
                  (agent_at ?l)
                  (not(dusted ?o ?l)))
 :effect(and(dusted ?o ?l)(increase (total-cost) 100))
)


(:action VacuumHouse ;working
 :parameters()
 :precondition(and(agent_at livingRoom)
                  (obj_at VacuumCleaner livingRoom)
                  (switched_on VacuumCleaner livingRoom)
                  (not(CleanedHouse)))
 :effect(and(CleanedHouse) 
            (increase (total-cost) 60))
)



 
(:action clean_edible ;working
 :parameters (?o1 - obj)
 :precondition (and(agent_at Kitchen)
                   (stuff_at ?o1 Basin Kitchen)
                   (not(In_hand ?o1))
                   (not(cleaned ?o1))
                   ;(switched_on Faucet Kitchen)
                )

 :effect(and(cleaned ?o1)
            (increase (total-cost) 8))
)

(:action slice ;working
 :parameters(?o1 ?o2 - obj)
 :precondition (and (agent_at Kitchen)
                    (stuff_at ?o1 CounterTop Kitchen)
                    (not(In_hand ?o1))
                    (not(In_hand ?o2))
                    (not(sliced ?o2))
                    (cleaned ?o1)
                    (equal ?o1 ?o2)
                )
 :effect (and(sliced ?o2)
             (stuff_at ?o2 CounterTop Kitchen)
             (increase (total-cost) 20)
         )                 
)

(:action cook ;working
 :parameters( ?o1 ?o3 - obj)
 :precondition (and (agent_at Kitchen)
                    (stuff_at ?o1 Stove Kitchen)
                    (equal ?o1 ?o3)
                    (not(cooked ?o3))
                    (switched_on burner Kitchen) 
                )
 :effect (and(cooked ?o3)
             (stuff_at ?o3 Stove Kitchen)
             (increase (total-cost) 120)
         )                 
)

(:action serve_food ;working
 :parameters(?o1 - food ?l - location)
 :precondition(and(agent_at ?l)
                  (cooked ?o1)
                  ;(switched_on Television ?l)
                  (stuff_at ?o1 plate ?l)
                  (not(In_hand ?o1))
                  (not(food_served ?o1 ?l))
              )
 :effect(and(food_served ?o1 ?l)
            (obj_at ?o1 ?l)
            (stuff_at remaining_food plate ?l)
            (increase (total-cost) 8)
        )
)


(:action BakeACake ;working
 :parameters(?o1 ?o3 - tobake)
 :precondition (and (agent_at Kitchen)
                    (stuff_at ?o1 Oven Kitchen)
                    ;(not(In_hand ?o1))
                    ;(not(In_hand ?o3))
                    (not(baked ?o3))
                    (switched_on Oven_switch Kitchen)
                    (equal ?o1 ?o3)   
                )
 :effect (and(baked ?o3)
             (stuff_at ?o3 CounterTop Kitchen)
             (increase (total-cost) 120)
             
         )                 
)

(:action serve_fruit ;working
 :parameters (?o1 - fruit ?l - location )
 :precondition(and(agent_at ?l)
                  (sliced ?o1)
                  (switched_on Television ?l)
                  (stuff_at ?o1 plate ?l) 
                  (not(In_hand ?o1))
                  (not(fruit_served ?o1 ?l))
              )
 :effect(and(fruit_served ?o1 ?l)
            (obj_at ?o1 ?l)
            (stuff_at Remaining_fruit plate ?l)
            (increase (total-cost) 8)
        )
)


(:action serve_vegetable ;working
 :parameters (?o1 - vegetable ?l - location )
 :precondition(and(agent_at ?l)
                  (cleaned ?o1)
                  (cooked ?o1)
                  ;(switched_on Television ?l)
                  (stuff_at ?o1 plate ?l) 
                  (not(In_hand ?o1))
                  (not(veggy_served ?o1 ?l))
              )
 :effect(and(veggy_served ?o1 ?l)
            (obj_at ?o1 ?l)
            (stuff_at Remaining_veggy plate ?l)
            (increase (total-cost) 8)
        )
)



(:action serve_baked ;working
 :parameters(?o1 - tobake ?l - location )
 :precondition(and(agent_at ?l)
                  (baked ?o1)
                  (stuff_at ?o1 plate ?l)
                  (switched_on Television ?l) 
                  (not(In_hand ?o1))
                  (not(baked_served ?o1 ?l))
             )
 :effect(and(baked_served ?o1 ?l)
            (obj_at ?o1 ?l)
            (stuff_at Remaining_baked plate ?l)
            (increase (total-cost) 8)
        )
)


(:action Serve_Drink ;working
 :parameters (?o - drink ?l - location)
 :precondition(and(agent_at ?l)
                  (stuff_at ?o glass ?l)
                  (not(served_drink ?o ?l))
            ) 
 :effect(and(served_drink ?o ?l)
            (increase (total-cost) 8)
        )
)



(:action Cleaned_remaining_food ;Doesnt clean drinks
 :parameters (?o1 - obj ?l - location)
 :precondition(and(food_remaining)
                  (stuff_at ?o1 Dustbin_1 Kitchen)
                  (not(cleaned_food ?o1 ?l))
              )
 :effect(and(cleaned_food ?o1 ?l)
            (increase (total-cost) 3))
)


(:action Drop
 :parameters(?o1 - obj ?l - location ?r - receptacle )
 :precondition(and(obj_at ?o1 ?l)
                  (receptacle_at ?r ?l)
                  (open ?r ?l)
                  (not(dropped ?o1 ?r ?l))
 ) 
 :effect(dropped ?o1 ?r ?l)
)

(:action WashingClothes  ;working            
 :parameters ()
 :precondition (and
                   (stuff_at Clothes WashingMachine Pantry)
                   (not(washed Clothes))
                   (switched_on WashingMachine_switch Pantry) 
               )
 :effect(and(washed Clothes)
            (stuff_at Cleaned_clothes WashingMachine Pantry)
            (increase (total-cost) 200)
)
)


(:action DryClothes    ;working
 :parameters( )
 :precondition(and(agent_at Pantry)
                  (stuff_at Cleaned_clothes Dryer Pantry)
                  (not(Dried Cleaned_clothes)))
 :effect(and(Dried Cleaned_clothes)(increase (total-cost) 120))
)


(:action Iron_Clothes  ;working
 :parameters()
 :precondition(and(Dried Cleaned_clothes)
                  (stuff_at Cleaned_clothes IroningBoard Bedroom)
                  (agent_at Bedroom)
                  (not(IronedClothes))
                  )
 :effect(and(IronedClothes)
            (stuff_at Ironed_clothes IroningBoard Bedroom)
            (increase (total-cost) 60)
))


(:action FoldClothes ;working
 :parameters()
 :precondition(and(Ironedclothes)
                  (obj_at Ironed_clothes Bedroom)
                  (not(clothes_folded)))
 :effect(and(clothes_folded)  
            (stuff_at folded_clothes IroningBoard Bedroom)
            (increase (total-cost) 10)
))


(:action Laundry_Done ;working
 :parameters()
 :precondition(and(stuff_at folded_clothes Closet Bedroom)
 (not(laundrydone))
 ) 
 :effect(and(laundrydone)(increase (total-cost) 2))
)


(:action water_the_plants ;working
 :parameters ()
 :precondition(and
               (agent_at Garden)
               (In_hand watering_hose)
               (switched_on watering_hose Garden)
               (not(watering_plants))  
              )
 :effect(and(watering_plants)
            (increase (total-cost) 20))
)



(:action cutting_the_grass ;working
 :parameters ()
 :precondition(and(agent_at garden)
                  (obj_at LawnMower Garden)
                  (switched_on LawnMower Garden)
                  (not(cutting_done))
 ) 
 :effect(and(cutting_done)(increase (total-cost) 100)
))


(:action Trash_Cleared ;working
 :parameters ()
 :precondition(and(stuff_at trash_1 Master_Dustbin Garden)
                  (stuff_at trash_2 Master_Dustbin Garden)
                  (not(Trash_cleared))
 )
 :effect(and(Trash_cleared)(increase (total-cost) 2))
)


(:action WashingDishes ;working
 :parameters()
 :precondition(and
          (stuff_at Dirtydishes Dishwasher Kitchen)
          (switched_on Dishwasher_Switch Kitchen)
          (not(dishes_cleaned))
 ) 
 :effect(and(dishes_cleaned)
            (stuff_at cleaned_dishes Dishwasher Kitchen)
            (increase (total-cost) 20)
            )
)



(:action Dim_the_lights
 :parameters(?l - location)
 :precondition (and(agent_at ?l)
                   (not(Dim_the_lights ?l))
 )
 :effect(and(Dim_the_lights ?l)(increase (total-cost) 5)
 ))


(:action Start_Movie
:parameters()
:precondition (and(Dim_the_lights Bedroom)
                  (switched_on Television Bedroom)
                  (not(movie_started))  
              )    
:effect(and(movie_started)(increase (total-cost) 3))

)


(:action Extinguish_Fire
 :parameters ()
 :precondition (and(obj_at extinguisher Kitchen)
                   (agent_at Kitchen)
                   (switched_on extinguisher Kitchen)
                   (not(FireExtinguished)
               ))
 :effect(and(FireExtinguished)(increase (total-cost) 10))
)


)




 

