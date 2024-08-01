from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(
        self, 
        entities: Set[Entity], 
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity
    ):
        self.entites = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()
        
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
            
            self.update_fov() # Update the FOv before the player's next action
    
    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view"""
        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8
        )
        # If a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console, context: Context):
        self.game_map.render(console)
        for entity in self.entites:
            # Only print entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
            
        context.present(console)
        
        console.clear()