

set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}")
set(CPACK_COMMAND_PRODUCTBUILD "${OSQUERY_DATA_PATH}/control/pkg/productbuild.sh")
set(CPACK_COMMAND_PKGBUILD "${CPACK_COMMAND_PRODUCTBUILD}")


# Set the path to the background image file
set(CPACK_PRODUCTBUILD_BACKGROUND "${CMAKE_SOURCE_DIR}/Resources/background.png")

# Set the alignment attribute for the background image
set(CPACK_PRODUCTBUILD_BACKGROUND_ALIGNMENT "center")

# Set the scaling attribute for the background image
set(CPACK_PRODUCTBUILD_BACKGROUND_SCALING "none")

# Set the MIME type of the background image
set(CPACK_PRODUCTBUILD_BACKGROUND_MIME_TYPE "image/png")

# Set the UTI type of the background image
set(CPACK_PRODUCTBUILD_BACKGROUND_UTI "public.png")

# Set the path to the background image file for the Dark Aqua theme
set(CPACK_PRODUCTBUILD_BACKGROUND_DARKAQUA "${CMAKE_SOURCE_DIR}/Resources/dark_aqua_background.png")

# Set the alignment attribute for the Dark Aqua background image
set(CPACK_PRODUCTBUILD_BACKGROUND_DARKAQUA_ALIGNMENT "center")

# Set the scaling attribute for the Dark Aqua background image
set(CPACK_PRODUCTBUILD_BACKGROUND_DARKAQUA_SCALING "none")

# Set the MIME type of the Dark Aqua background image
set(CPACK_PRODUCTBUILD_BACKGROUND_DARKAQUA_MIME_TYPE "image/png")

# Set the UTI type of the Dark Aqua background image
set(CPACK_PRODUCTBUILD_BACKGROUND_DARKAQUA_UTI "public.png")


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
    "${CMAKE_SOURCE_DIR}/Resources/images/vistar.ico"
    "${CMAKE_SOURCE_DIR}/Resources/images/toggle_on.ico"
    "${CMAKE_SOURCE_DIR}/Resources/images/toggle_off.ico"
    "${CMAKE_SOURCE_DIR}/Resources/images/login.ico"
    

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
