# AI2THOR SIMULATION DESCRIPTION

AI2THOR is a simulation environment and an open source platform for Visual AI. It is developed by Allen AI. More information about the simulator and it's installation information can be viewed in their [github link](https://github.com/allenai/ai2thor).

Following links give a clear idea about the functions that can be used for interaction of the robot with the environment:
* [Object Interaction](https://allenai.github.io/ai2thor-v2.1.0-documentation/actions/interaction)
* [Held Object Manipulation](https://allenai.github.io/ai2thor-v2.1.0-documentation/actions/held)
* [Object Types](https://ai2thor.allenai.org/ithor/documentation/objects/object-types/)
* [Agent Navigation](https://allenai.github.io/ai2thor-v2.1.0-documentation/actions/navigation)
* [Control/Event Data](https://allenai.github.io/ai2thor-v2.1.0-documentation/event-metadata)
* [Miscellaneous Actions](https://allenai.github.io/ai2thor-v2.1.0-documentation/actions/misc)


### Task Anticipation

The robot in the environment carries out tasks in such a fashion where it reduces the overall time to carry out main tasks (like cooking, washing, serving, etc).

With Task Anticipation | Without Task Anticipation
:-: | :-:
<video width="700" height="300" src="https://github.com/AnticipateAndAct/AnticipateAndAct/blob/main/ai2thor/assets/Task_Anticipation.mp4"></video> | <video width="700" height="300" src="https://github.com/AnticipateAndAct/AnticipateAndAct/blob/main/ai2thor/assets/Without_Task_Anticipation.mp4"></video>
**Initial State** <br> 1) Apple -> CounterTop2, 2) Tomato -> Fridge, 3) Potato -> CounterTop2, Pot -> CounterTop1, 4) Knife -> CounterTop1 | **Initial State** <br>  1) Apple -> CounterTop2, 2) Tomato -> Fridge, 3) Potato -> CounterTop2, Pot -> CounterTop1, 4) Knife -> CounterTop1
**Final State** <br>  1) Apple -> Fridge, 2) Tomato -> CounterTop2, 3) Potato -> Pot -> StoveBurner, 4) Knife -> Drawer5 | **Final State** <br>  1) Apple -> Fridge, 2) Knife -> Drawer5, 3) Potato -> Pot -> StoveBurner, 4) Tomato -> CounterTop2
**Steps** <br> 1) Pick Apple and put it in the fridge <br> 2) Pick the Tomato in the fridge and place it on CounterTop2 <br> 3) Pick the Potato placed on the CounterTop2 and place it inside the pot filled with water and keep the pot on the StoveBurner and start Boiling <br> 4) Keep the Knife present on the CounterTop1 inside the Drawer5 | **Steps** <br> 1) Pick Apple and put it in the fridge <br> 2) Keep the Knife present on the CounterTop1 inside the Drawer5 <br> 3) Pick the Potato placed on the CounterTop2 and place it inside the pot filled with water and keep the pot on the StoveBurner and start Boiling <br> 4) Pick the Tomato in the fridge and place it on CounterTop2

The simulation shows a significant difference in the amount of time it takes for the robot to complete 4 tasks


