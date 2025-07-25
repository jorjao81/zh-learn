"""
Character decomposition module for extracting Chinese character components.
Uses Hanzipy library for radical extraction and component analysis.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ComponentType(Enum):
    SEMANTIC = "semantic"
    PHONETIC = "phonetic"
    PICTOGRAPHIC = "pictographic"
    UNKNOWN = "unknown"


@dataclass
class ComponentResult:
    character: str
    components: List[str]
    radical_meanings: List[str]
    component_types: List[ComponentType]
    component_pinyin: List[Optional[str]]
    structure_notes: str


class CharacterDecomposer:
    """Extract main components from Chinese characters using Hanzipy."""

    def __init__(self) -> None:
        # Import here to handle potential import errors gracefully
        try:
            from hanzipy.decomposer import HanziDecomposer
            from pypinyin import pinyin, Style

            self.decomposer = HanziDecomposer()
            self.pinyin = pinyin
            self.pinyin_style = Style.TONE
        except ImportError as e:
            if "hanzipy" in str(e):
                raise ImportError(
                    "Hanzipy library is required. Install with: pip install hanzipy"
                )
            elif "pypinyin" in str(e):
                raise ImportError(
                    "pypinyin library is required. Install with: pip install pypinyin"
                )
            else:
                raise e

    def decompose(self, character: str) -> ComponentResult:
        """
        Extract main components from a single Chinese character.

        Args:
            character: Single Chinese character to decompose

        Returns:
            ComponentResult with components, meanings, and structure analysis
        """
        if not character or len(character) != 1:
            raise ValueError("Input must be a single Chinese character")

        # Get components from Hanzipy
        components = self._get_components(character)

        # Get meanings for each component
        meanings = [self._get_radical_meaning(comp) for comp in components]

        # Classify component types
        component_types = [
            self._classify_component(comp, character) for comp in components
        ]

        # Get pinyin for phonetic components
        component_pinyin = [
            self._get_component_pinyin(comp, comp_type)
            for comp, comp_type in zip(components, component_types)
        ]

        # Generate structure notes
        structure_notes = self._generate_structure_notes(
            character, components, component_types, component_pinyin
        )

        return ComponentResult(
            character=character,
            components=components,
            radical_meanings=meanings,
            component_types=component_types,
            component_pinyin=component_pinyin,
            structure_notes=structure_notes,
        )

    def _get_components(self, character: str) -> List[str]:
        """Extract components using Hanzipy decomposer."""
        try:
            components = self.decomposer.get_components(character)
            return components if components else [character]
        except Exception:
            # If decomposition fails, return the character itself
            return [character]

    def _get_radical_meaning(self, radical: str) -> str:
        """Get meaning of a radical using Hanzipy."""
        # Common radical meanings not covered by Hanzipy
        common_meanings = {
            "氵": "water",
            "亻": "person",
            "扌": "hand",
            "忄": "heart",
            "艹": "grass",
            "犭": "dog",
            "阝": "city/mound",
            "讠": "speech",
            "饣": "food",
            "衤": "clothes",
            "疒": "sickness",
            "宀": "roof",
            "冫": "ice",
            "日": "sun/day",
            "月": "moon",
            "木": "tree",
            "火": "fire",
            "土": "earth",
            "石": "stone",
            "金": "metal",
            "女": "woman",
            "子": "child",
            "心": "heart",
            "手": "hand",
            "口": "mouth",
            "目": "eye",
            "人": "person",
        }

        if radical in common_meanings:
            return common_meanings[radical]

        try:
            meaning = self.decomposer.get_radical_meaning(radical)
            return meaning if meaning else "unknown"
        except Exception:
            return "unknown"

    def _get_component_pinyin(
        self, component: str, component_type: ComponentType
    ) -> Optional[str]:
        """Get pinyin for phonetic/unknown components, Chinese names for semantic components."""
        # For phonetic and unknown components, always use pinyin
        if component_type in (ComponentType.PHONETIC, ComponentType.UNKNOWN):
            try:
                pinyin_result = self.pinyin(component, style=self.pinyin_style)
                if pinyin_result and pinyin_result[0]:
                    return pinyin_result[0][0]
            except Exception:
                pass
            return None

        # For semantic components, use Chinese names for radicals
        # Chinese names for common Kangxi radicals
        radical_chinese_names = {
            # Water radicals
            "氵": "三点水",  # san dian shui
            "水": "水字底",  # shui zi di
            # Person radicals
            "亻": "单人旁",  # dan ren pang
            "人": "人字头",  # ren zi tou
            # Hand radicals
            "扌": "提手旁",  # ti shou pang
            "手": "手字旁",  # shou zi pang
            # Heart radicals
            "忄": "竖心旁",  # shu xin pang
            "心": "心字底",  # xin zi di
            # Speech radical
            "讠": "言字旁",  # yan zi pang
            # Food radical
            "饣": "食字旁",  # shi zi pang
            # Clothes radical
            "衤": "衣字旁",  # yi zi pang
            # Grass radical
            "艹": "草字头",  # cao zi tou
            # Dog radical
            "犭": "反犬旁",  # fan quan pang
            # City radical
            "阝": "双耳旁",  # shuang er pang (left) / "右耳旁" (right)
            # Sickness radical
            "疒": "病字头",  # bing zi tou
            # Roof radical
            "宀": "宝盖头",  # bao gai tou
            # Ice radical
            "冫": "两点水",  # liang dian shui
            # Fire radical
            "灬": "四点底",  # si dian di
            # Jade radical
            "王": "王字旁",  # wang zi pang
            # Stone radical
            "石": "石字旁",  # shi zi pang
            # Wood radical
            "木": "木字旁",  # mu zi pang
            # Metal radical
            "钅": "金字旁",  # jin zi pang
            # Earth radical
            "土": "土字旁",  # tu zi pang
            # Sun radical
            "日": "日字旁",  # ri zi pang
            # Moon radical
            "月": "月字旁",  # yue zi pang
            # Eye radical
            "目": "目字旁",  # mu zi pang
            # Mouth radical
            "口": "口字旁",  # kou zi pang
            # Woman radical
            "女": "女字旁",  # nv zi pang
            # Child radical
            "子": "子字旁",  # zi zi pang
            # Silk radical
            "纟": "绞丝旁",  # jiao si pang
            # Thread radical
            "糸": "绞丝底",  # jiao si di
            # Foot radical
            "足": "足字旁",  # zu zi pang
            # Walk radical
            "辶": "走之旁",  # zou zhi pang
            # Door radical
            "门": "门字框",  # men zi kuang
            # Enclosure radical
            "囗": "国字框",  # guo zi kuang
            # Mountain radical
            "山": "山字旁",  # shan zi pang
            # Work radical
            "工": "工字旁",  # gong zi pang
            # Bow radical
            "弓": "弓字旁",  # gong zi pang
            # Step radical
            "彳": "双人旁",  # shuang ren pang
            # Knife radical
            "刀": "刀字旁",  # dao zi pang
            "刂": "立刀旁",  # li dao pang
            # Power radical
            "力": "力字旁",  # li zi pang
            # Vehicle radical
            "车": "车字旁",  # che zi pang
            # Horse radical
            "马": "马字旁",  # ma zi pang
            # Bird radical
            "鸟": "鸟字旁",  # niao zi pang
            # Fish radical
            "鱼": "鱼字旁",  # yu zi pang
            # Insect radical
            "虫": "虫字旁",  # chong zi pang
            # Grain radical
            "禾": "禾字旁",  # he zi pang
            # Bamboo radical
            "竹": "竹字头",  # zhu zi tou
            # Net radical
            "网": "四字头",  # si zi tou
            # Leather radical
            "革": "革字旁",  # ge zi pang
            # Page radical
            "页": "页字旁",  # ye zi pang
            # Wind radical
            "风": "风字旁",  # feng zi pang
            # Rain radical
            "雨": "雨字头",  # yu zi tou
            # Food radical (full form)
            "食": "食字旁",  # shi zi pang
        }

        # Check if component has a Chinese radical name
        if component in radical_chinese_names:
            return radical_chinese_names[component]

        # Fall back to pinyin for semantic components without Chinese names
        try:
            pinyin_result = self.pinyin(component, style=self.pinyin_style)
            if pinyin_result and pinyin_result[0]:
                return pinyin_result[0][0]
        except Exception:
            pass
        return None

    def _classify_component(
        self, component: str, original_character: str
    ) -> ComponentType:
        """
        Classify component as semantic, phonetic, or pictographic.
        This is a simplified heuristic-based classification.
        """
        # Common semantic radicals (simplified heuristic)
        semantic_radicals = {
            "氵": ComponentType.SEMANTIC,  # water
            "木": ComponentType.SEMANTIC,  # wood
            "火": ComponentType.SEMANTIC,  # fire
            "土": ComponentType.SEMANTIC,  # earth
            "金": ComponentType.SEMANTIC,  # metal
            "女": ComponentType.SEMANTIC,  # woman
            "子": ComponentType.SEMANTIC,  # child
            "心": ComponentType.SEMANTIC,  # heart
            "忄": ComponentType.SEMANTIC,  # heart radical
            "手": ComponentType.SEMANTIC,  # hand
            "扌": ComponentType.SEMANTIC,  # hand radical
            "口": ComponentType.SEMANTIC,  # mouth
            "目": ComponentType.SEMANTIC,  # eye
            "日": ComponentType.SEMANTIC,  # sun
            "月": ComponentType.SEMANTIC,  # moon
            "人": ComponentType.SEMANTIC,  # person
            "亻": ComponentType.SEMANTIC,  # person radical
            "艹": ComponentType.SEMANTIC,  # grass radical
            "犭": ComponentType.SEMANTIC,  # dog radical
            "阝": ComponentType.SEMANTIC,  # city radical
            "讠": ComponentType.SEMANTIC,  # speech radical
            "饣": ComponentType.SEMANTIC,  # food radical
            "衤": ComponentType.SEMANTIC,  # clothes radical
            "疒": ComponentType.SEMANTIC,  # sickness radical
            "石": ComponentType.SEMANTIC,  # stone
            "宀": ComponentType.SEMANTIC,  # roof radical
            "冫": ComponentType.SEMANTIC,  # ice radical
        }

        if component in semantic_radicals:
            return semantic_radicals[component]

        # If component is same as original character, it's pictographic
        if component == original_character:
            return ComponentType.PICTOGRAPHIC

        # For components that are not semantic radicals and not the same as original character,
        # they are likely phonetic components (providing sound)
        return ComponentType.PHONETIC

    def _generate_structure_notes(
        self,
        character: str,
        components: List[str],
        component_types: List[ComponentType],
        component_pinyin: List[Optional[str]],
    ) -> str:
        """Generate human-readable structure explanation."""
        if len(components) == 1:
            return f"Simple character: {character}"

        if len(components) == 2:
            type1, type2 = component_types[0], component_types[1]
            comp1, comp2 = components[0], components[1]
            pinyin1, pinyin2 = component_pinyin[0], component_pinyin[1]

            if type1 == ComponentType.SEMANTIC and type2 == ComponentType.SEMANTIC:
                pinyin1_note = f" ({pinyin1})" if pinyin1 else ""
                pinyin2_note = f" ({pinyin2})" if pinyin2 else ""
                return f"{comp1}{pinyin1_note} + {comp2}{pinyin2_note}"
            elif type1 == ComponentType.SEMANTIC and type2 == ComponentType.PHONETIC:
                pinyin1_note = f" ({pinyin1})" if pinyin1 else ""
                pinyin2_note = f" ({pinyin2})" if pinyin2 else ""
                return (
                    f"{comp1}{pinyin1_note} (meaning) + {comp2}{pinyin2_note} (sound)"
                )
            elif type1 == ComponentType.PHONETIC and type2 == ComponentType.SEMANTIC:
                pinyin1_note = f" ({pinyin1})" if pinyin1 else ""
                pinyin2_note = f" ({pinyin2})" if pinyin2 else ""
                return (
                    f"{comp1}{pinyin1_note} (sound) + {comp2}{pinyin2_note} (meaning)"
                )
            else:
                # For unknown types, show both pinyin and meaning
                comp1_info = self._get_component_full_info(
                    comp1, pinyin1, component_types[0]
                )
                comp2_info = self._get_component_full_info(
                    comp2, pinyin2, component_types[1]
                )
                return f"{comp1_info} + {comp2_info}"

        return f"Complex character with {len(components)} components: {' + '.join(components)}"

    def _get_component_full_info(
        self, component: str, pinyin: Optional[str], component_type: ComponentType
    ) -> str:
        """Get full component information with both pinyin and meaning for unknown types."""
        # Get the meaning for this component
        meaning = self._get_radical_meaning(component)

        # Get pinyin if not provided
        if not pinyin:
            try:
                pinyin_result = self.pinyin(component, style=self.pinyin_style)
                if pinyin_result and pinyin_result[0]:
                    pinyin = pinyin_result[0][0]
            except Exception:
                pass

        # Format based on type
        if component_type == ComponentType.UNKNOWN:
            # For unknown types, show both pinyin and meaning
            if pinyin and meaning and meaning != "unknown":
                return f"{component} ({pinyin} - {meaning})"
            elif pinyin:
                return f"{component} ({pinyin})"
            elif meaning and meaning != "unknown":
                return f"{component} ({meaning})"
            else:
                return component
        else:
            # For known types, use existing logic
            if component_type == ComponentType.SEMANTIC:
                return f"{component} ({pinyin})" if pinyin else component
            elif component_type == ComponentType.PHONETIC:
                return f"{component} ({pinyin})" if pinyin else component
            else:
                return component
