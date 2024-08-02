from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine
    
MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # WASD keys.
    tcod.event.KeySym.w: (0, -1),
    tcod.event.KeySym.s: (0, 1),
    tcod.event.KeySym.a: (-1, 0),
    tcod.event.KeySym.d: (1, 0),
    tcod.event.KeySym.q: (-1, -1),
    tcod.event.KeySym.z: (-1, 1),
    tcod.event.KeySym.e: (1, -1),
    tcod.event.KeySym.c: (1, 1),
    # Vi keys.
    tcod.event.KeySym.h: (0, -1),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.k: (-1, 0),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.u: (-1, 1),
    tcod.event.KeySym.b: (1, -1),
    tcod.event.KeySym.n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.x,
    tcod.event.KeySym.SPACE
}

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def handle_events(self) -> None:
        raise NotImplementedError()
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    
    
class MainGameEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            
            if action is None:
                continue
            
            action.perform()
            
            self.engine.handle_enemy_turns()
            self.engine.update_fov()
            
            
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
    
        key = event.sym
        
        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)
            
        # No valid key was pressed
        return action
    
class GameOVerEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            
            if action is None:
                continue
            
            action.perform()
            
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Optional[Action] = None
        
        key = event.sym
        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)
            
        # No valid key was pressed
        return action