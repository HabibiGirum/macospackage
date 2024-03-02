

set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}")
set(CPACK_COMMAND_PRODUCTBUILD "${OSQUERY_DATA_PATH}/control/pkg/productbuild.sh")
set(CPACK_COMMAND_PKGBUILD "${CPACK_COMMAND_PRODUCTBUILD}")

install(
  FILES
    "${CMAKE_SOURCE_DIR}/Resources/Info.plist"
    

  DESTINATION
    "/Applications/Vistar.app/Contents"

  COMPONENT
    osquery
)

install(
  FILES
    "${CMAKE_SOURCE_DIR}/Resources/io.vistar.agent.plist"

  DESTINATION
    "/Library/LaunchDaemons/"

  COMPONENT
    osquery
)

install(
  FILES
    "${CMAKE_SOURCE_DIR}/Resources/vistarlogo.png"
    "${CMAKE_SOURCE_DIR}/Resources/toggle_on.png"
    "${CMAKE_SOURCE_DIR}/Resources/toggle_off.png"
    "${CMAKE_SOURCE_DIR}/Resources/login.png"
    

  DESTINATION
    "/Applications/Vistar.app/Contents/Resources"

  COMPONENT
    osquery
)

install(
  CODE
    "execute_process(COMMAND chmod +x /Applications/Vistar.app/Contents/MacOS/Vistar)"
  COMPONENT osquery
)
