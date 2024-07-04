project(FCC-config)

include(GNUInstallDirs)

install(DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/FCCee/ DESTINATION ${CMAKE_INSTALL_DATADIR}/${CMAKE_PROJECT_NAME})

# TESTING
find_program(BASH_PROGRAM bash)
include(CTest)
#if (BASH_PROGRAM)
#  add_test(NAME ALLEGRO_o1_v03 COMMAND ${BASH_PROGRAM} FCCee/FullSim/ALLEGRO/ALLEGRO_o1_v03/run_sim_digi_reco.sh)
#endif()
add_test(NAME ALLEGRO_o1_v03 COMMAND ../FCCee/FullSim/ALLEGRO/ALLEGRO_o1_v03/run_sim_digi_reco.sh)
