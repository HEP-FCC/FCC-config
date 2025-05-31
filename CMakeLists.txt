CMAKE_MINIMUM_REQUIRED(VERSION 3.12)

project(FCC-config LANGUAGES CXX)

include(GNUInstallDirs)

install(DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/FCCee/ DESTINATION ${CMAKE_INSTALL_DATADIR}/${CMAKE_PROJECT_NAME})

# TESTING
include(CTest)
add_test(NAME ALLEGRO_o1_v03 COMMAND ../FCCee/FullSim/ALLEGRO/ALLEGRO_o1_v03/ctest_sim_digi_reco.sh)
add_test(NAME IDEA_o1_v03 COMMAND ../FCCee/FullSim/IDEA/IDEA_o1_v03/ctest_sim_digi_reco.sh)
