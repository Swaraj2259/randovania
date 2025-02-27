from __future__ import annotations

from typing import TYPE_CHECKING

from randovania.exporter.hints.hint_formatters import RelativeAreaFormatter, TemplatedFormatter
from randovania.exporter.hints.hint_namer import HintNamer, PickupLocation
from randovania.exporter.hints.relative_item_formatter import RelativeItemFormatter
from randovania.game_description import default_database
from randovania.game_description.hint import HintLocationPrecision, LocationHint

if TYPE_CHECKING:
    from randovania.exporter.hints.pickup_hint import PickupHint
    from randovania.game.game_enum import RandovaniaGame
    from randovania.game_description.game_patches import GamePatches
    from randovania.game_description.resources.item_resource_info import ItemResourceInfo
    from randovania.interface_common.players_configuration import PlayersConfiguration


class CSHintNamer(HintNamer):
    def __init__(self, all_patches: dict[int, GamePatches], players_config: PlayersConfiguration):
        patches = all_patches[players_config.player_index]

        self.location_formatters = {
            HintLocationPrecision.MALCO: TemplatedFormatter(
                "BUT ALL I KNOW HOW TO DO IS MAKE {determiner.upper}{pickup}...", self, upper_pickup=True
            ),
            HintLocationPrecision.JENKA: TemplatedFormatter(
                "perhaps I'll give you {determiner}{pickup} in return...", self
            ),
            HintLocationPrecision.LITTLE: TemplatedFormatter(
                "He was exploring the island with {determiner}{pickup}...", self
            ),
            HintLocationPrecision.NUMAHACHI: TemplatedFormatter("{determiner.capitalize}{pickup}.", self),
            HintLocationPrecision.DETAILED: TemplatedFormatter(
                "{{start}} {determiner}{pickup} {{mid}} in {node}.", self
            ),
            HintLocationPrecision.REGION_ONLY: TemplatedFormatter(
                "{{start}} {determiner}{pickup} {{mid}} in {node}.", self
            ),
            HintLocationPrecision.RELATIVE_TO_AREA: RelativeAreaFormatter(
                patches,
                lambda msg, with_color: msg,
            ),
            HintLocationPrecision.RELATIVE_TO_INDEX: RelativeItemFormatter(
                patches,
                lambda msg, with_color: msg,
                players_config,
            ),
        }

    def format_joke(self, joke: str, with_color: bool) -> str:
        return joke

    def format_player(self, name: str, with_color: bool) -> str:
        return name

    def format_region(self, location: PickupLocation, with_color: bool) -> str:
        region_list = default_database.game_description_for(location.game).region_list
        return region_list.region_name_from_node(region_list.node_from_pickup_index(location.location), True)

    def format_area(self, location: PickupLocation, with_region: bool, with_color: bool) -> str:
        region_list = default_database.game_description_for(location.game).region_list
        area = region_list.nodes_to_area(region_list.node_from_pickup_index(location.location))
        return area.name

    def format_location_hint(
        self, game: RandovaniaGame, pick_hint: PickupHint, hint: LocationHint, with_color: bool
    ) -> str:
        return self.location_formatters[hint.precision.location].format(
            game,
            pick_hint,
            hint,
            with_color,
        )

    def format_resource_is_starting(self, resource: ItemResourceInfo, with_color: bool) -> str:
        # TODO
        raise RuntimeError("Not implemented")

    def format_guaranteed_resource(
        self,
        resource: ItemResourceInfo,
        player_name: str | None,
        location: PickupLocation,
        hide_area: bool,
        with_color: bool,
    ) -> str:
        # TODO
        raise RuntimeError("Not implemented")

    def format_temple_name(self, temple_name: str, with_color: bool) -> str:
        raise RuntimeError("Unsupported function")
