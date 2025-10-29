from puzzle_solver.puzzles.aquarium import aquarium as aquarium_solver
from puzzle_solver.puzzles.battleships import battleships as battleships_solver
from puzzle_solver.puzzles.binairo import binairo as binairo_solver
from puzzle_solver.puzzles.binairo import binairo_plus as binairo_plus_solver
from puzzle_solver.puzzles.black_box import black_box as black_box_solver
from puzzle_solver.puzzles.bridges import bridges as bridges_solver
from puzzle_solver.puzzles.chess_range import chess_range as chess_range_solver
from puzzle_solver.puzzles.chess_range import chess_solo as chess_solo_solver
from puzzle_solver.puzzles.chess_range import chess_melee as chess_melee_solver
from puzzle_solver.puzzles.connect_the_dots import connect_the_dots as connect_the_dots_solver
from puzzle_solver.puzzles.dominosa import dominosa as dominosa_solver
from puzzle_solver.puzzles.filling import filling as filling_solver
from puzzle_solver.puzzles.flood_it import flood_it as flood_it_solver
from puzzle_solver.puzzles.flip import flip as flip_solver
from puzzle_solver.puzzles.galaxies import galaxies as galaxies_solver
from puzzle_solver.puzzles.guess import guess as guess_solver
from puzzle_solver.puzzles.heyawake import heyawake as heyawake_solver
from puzzle_solver.puzzles.inertia import inertia as inertia_solver
from puzzle_solver.puzzles.kakurasu import kakurasu as kakurasu_solver
from puzzle_solver.puzzles.kakuro import kakuro as kakuro_solver
from puzzle_solver.puzzles.keen import keen as keen_solver
from puzzle_solver.puzzles.light_up import light_up as light_up_solver
from puzzle_solver.puzzles.magnets import magnets as magnets_solver
from puzzle_solver.puzzles.map import map as map_solver
from puzzle_solver.puzzles.minesweeper import minesweeper as minesweeper_solver
from puzzle_solver.puzzles.mosaic import mosaic as mosaic_solver
from puzzle_solver.puzzles.nonograms import nonograms as nonograms_solver
from puzzle_solver.puzzles.nonograms import nonograms_colored as nonograms_colored_solver
from puzzle_solver.puzzles.norinori import norinori as norinori_solver
from puzzle_solver.puzzles.nurikabe import nurikabe as nurikabe_solver
from puzzle_solver.puzzles.palisade import palisade as palisade_solver
from puzzle_solver.puzzles.lits import lits as lits_solver
from puzzle_solver.puzzles.pearl import pearl as pearl_solver
from puzzle_solver.puzzles.pipes import pipes as pipes_solver
from puzzle_solver.puzzles.range import range as range_solver
from puzzle_solver.puzzles.rectangles import rectangles as rectangles_solver
from puzzle_solver.puzzles.shakashaka import shakashaka as shakashaka_solver
from puzzle_solver.puzzles.shingoki import shingoki as shingoki_solver
from puzzle_solver.puzzles.signpost import signpost as signpost_solver
from puzzle_solver.puzzles.singles import singles as singles_solver
from puzzle_solver.puzzles.slant import slant as slant_solver
from puzzle_solver.puzzles.slitherlink import slitherlink as slitherlink_solver
from puzzle_solver.puzzles.star_battle import star_battle as star_battle_solver
from puzzle_solver.puzzles.star_battle import star_battle_shapeless as star_battle_shapeless_solver
from puzzle_solver.puzzles.stitches import stitches as stitches_solver
from puzzle_solver.puzzles.sudoku import sudoku as sudoku_solver
from puzzle_solver.puzzles.tapa import tapa as tapa_solver
from puzzle_solver.puzzles.tents import tents as tents_solver
from puzzle_solver.puzzles.thermometers import thermometers as thermometers_solver
from puzzle_solver.puzzles.towers import towers as towers_solver
from puzzle_solver.puzzles.tracks import tracks as tracks_solver
from puzzle_solver.puzzles.twiddle import twiddle as twiddle_solver
from puzzle_solver.puzzles.undead import undead as undead_solver
from puzzle_solver.puzzles.unequal import unequal as unequal_solver
from puzzle_solver.puzzles.unruly import unruly as unruly_solver
from puzzle_solver.puzzles.yin_yang import yin_yang as yin_yang_solver

from puzzle_solver.puzzles.inertia.parse_map.parse_map import main as inertia_image_parser

__all__ = [
    aquarium_solver,
    battleships_solver,
    binairo_solver,
    binairo_plus_solver,
    black_box_solver,
    bridges_solver,
    chess_range_solver,
    chess_solo_solver,
    chess_melee_solver,
    connect_the_dots_solver,
    dominosa_solver,
    filling_solver,
    flood_it_solver,
    flip_solver,
    galaxies_solver,
    guess_solver,
    heyawake_solver,
    inertia_solver,
    kakurasu_solver,
    kakuro_solver,
    keen_solver,
    light_up_solver,
    magnets_solver,
    map_solver,
    minesweeper_solver,
    mosaic_solver,
    nonograms_solver,
    norinori_solver,
    nonograms_colored_solver,
    nurikabe_solver,
    palisade_solver,
    lits_solver,
    pearl_solver,
    pipes_solver,
    range_solver,
    rectangles_solver,
    shakashaka_solver,
    shingoki_solver,
    signpost_solver,
    singles_solver,
    slant_solver,
    slitherlink_solver,
    star_battle_solver,
    star_battle_shapeless_solver,
    stitches_solver,
    sudoku_solver,
    tapa_solver,
    tents_solver,
    thermometers_solver,
    towers_solver,
    tracks_solver,
    twiddle_solver,
    undead_solver,
    unequal_solver,
    unruly_solver,
    yin_yang_solver,
    inertia_image_parser,
]

__version__ = '1.0.4'
