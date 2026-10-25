## gh-protocol E2E log — 2026-10-25T05:50:26Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T05:41:22Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 05:38 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 05:41 .
drwxr-xr-x 3 runner runner 4096 Oct 25 05:41 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 05:41 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 05:41 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2883
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7fa853001000 as it is in the protected range from 0x7fa753000000 to 0x7fa853200000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Successfully initialized netsim WiFi
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 27469 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:processDebugResources
> Task :app:compressDebugAssets
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792906745602.json

BUILD SUCCESSFUL in 1m 59s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 60s) ==
WARN: emulator CANNOT reach raw.githubusercontent.com (runner NAT) — pre-seeding app cache
seeded cache: 37417 bytes, meta=1792906992951
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5693)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5693   339   14123128 175884 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp        0      0 10.0.2.16:60058         142.251.154.119:443     CLOSE_WAIT 
tcp      130      0 10.0.2.16:56782         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:60684         172.217.115.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:33930         142.251.151.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:56800         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:56768         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:56794         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:56790         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:52938         172.217.114.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:56788         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:36032         172.217.117.4:443       CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:42591  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:46725  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:34626  ::ffff:173.194.64.9:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:43678  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:42534  ::ffff:192.178.129.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:50298  ::ffff:216.239.36.1:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:52208  ::ffff:172.217.112.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:35246  ::ffff:192.178.129.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:36050  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:42066  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:57272  ::ffff:192.178.209.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:55286  ::ffff:172.217.112.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:42078  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:40178  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:42518  ::ffff:209.85.145.9:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:42072  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:36060  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:34614  ::ffff:173.194.64.9:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:36150  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:43352  ::ffff:192.178.212.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:59862  ::ffff:173.194.194.:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.16:58122  ::ffff:173.194.193:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:40774  ::ffff:172.217.113.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:43286  ::ffff:173.194.192.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:36036  ::ffff:142.251.157.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:52196  ::ffff:172.217.112.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:51384  ::ffff:172.217.113.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{4050b53 5693:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-7m2s710ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{4050b53 5693:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.2 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{3f2f9c6 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-7m9s996ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@266039996
  deepestLastOrientationSource=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.35 fontWeightAdjustment=0}
  mLayoutSeq=91
  mCurrentFocus=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{adb3d9a #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{5b1da39 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{bd3baa6 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{6b1b474 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{2b4e212 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{55af62e u0 StatusBar}
    mFocusedWindow=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=4cb60006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {4cb60000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=4cb60006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{55af62e u0 StatusBar}
--
        mWindowContainer=Window{55af62e u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=55af62e StatusBar)/@0xaa4473a - animation-leash of insets_animation)/@0x705eb3b
        mControlTarget=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=f0aea14 InputMethod)/@0x9665803 - animation-leash of insets_animation)/@0x5d35258 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{f0aea14 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=f0aea14 InputMethod)/@0x9665803 - animation-leash of insets_animation)/@0x5d35258
        mControlTarget=Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{45d5d9d #3 type=undefined}
        (multi-window) Task{2b4e212 #4 type=undefined}
        (fullscreen) Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{4050b53 5693:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray:
total 79624
drwx------ 2 u0_a192 u0_a192     4096 2026-10-25 05:43 .
drwxrwxrwx 3 u0_a192 u0_a192     4096 2026-10-25 05:43 ..
-rwx--x--x 1 u0_a192 u0_a192 38872056 2026-10-25 05:43 Xray
-rw------- 1 u0_a192 u0_a192 36282168 2026-10-25 05:43 Xray-arm64-v8a
-rw------- 1 u0_a192 u0_a192  3977011 2026-10-25 05:43 geoip.dat
-rw------- 1 u0_a192 u0_a192  2358471 2026-10-25 05:43 geosite.dat
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-25 05:43:20.998  5693  5693 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 05:43:20.999  5693  5693 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 05:43:21.300  5693  5693 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-25 05:43:21.300  5693  5693 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
id.os.BinderProxy@1d9f046 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=89633 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@d24d207} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{915bf34 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:43:12.837   526  1710 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 05:43:12.869   526   554 I ActivityManager: Start proc 5693:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 05:43:12.874   526  1710 D CoreBackPreview: Window{343a989 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@bca00c1, mPriority=0, mIsAnimationCallback=false}
10-25 05:43:12.899  5693  5693 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 05:43:12.995   526   543 V WindowManager: Sent Transition #6 createdAt=10-25 05:43:12.828 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=89633 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{7b4e7fd Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{1640cf2 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:43:12.998   526   543 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{7b4e7fd Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xa4c7fa7 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{8b76f43 Task{adb3d9a #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xa372bc4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:43:13.099  5693  5693 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 05:43:13.099  5693  5693 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 05:43:13.099  5693  5693 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 05:43:13.247  5693  5693 W ziparchive: Unable to open '/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.dm': No such file or directory
10-25 05:43:13.247  5693  5693 W ziparchive: Unable to open '/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.dm': No such file or directory
10-25 05:43:13.437  5693  5693 D nativeloader: Configuring clns-6 for other apk /data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/lib/x86_64:/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 05:43:13.442  5693  5693 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 05:43:13.443  5693  5693 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:43:13.652  5693  5693 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 05:43:13.681   526  1274 D CoreBackPreview: Window{3f2f9c6 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@c55cb23, mPriority=0, mIsAnimationCallback=false}
10-25 05:43:14.078   526   543 W ziparchive: Unable to open '/data/app/~~Cl-OaMl84eTcFWCUV5l1Jw==/com.ghprotocol.app-0pTYGj5qkNcgUyBtGb6w8w==/base.dm': No such file or directory
10-25 05:43:14.079   526   543 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s251ms
10-25 05:43:14.111   526  2286 I ImeTracker: com.ghprotocol.app:e9b9ff49: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 05:43:14.111   526  2286 I ImeTracker: com.ghprotocol.app:e9b9ff49: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 05:43:14.123   526  2286 W InputManager-JNI: Input channel object '343a989 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 05:43:14.124   526  1274 D CoreBackPreview: Window{343a989 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 05:43:14.128  1522  1522 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 05:43:15.286   526   577 I AppsFilter: interaction: PackageSetting{94fad35 com.ghprotocol.app/10192} -> PackageSetting{9b115ca com.google.android.contacts/10154} BLOCKED
10-25 05:43:18.829  5693  5788 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 05:43:20.906   526  2280 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 05:43:20.906   830   870 V WindowManagerShell: Transition requested: android.os.BinderProxy@1df6539 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=97702 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@ba77e} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b72e4df com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:43:20.998  5693  5693 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 05:43:20.999  5693  5693 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 05:43:21.300  5693  5693 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-25 05:43:21.300  5693  5693 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
10-25 05:43:21.294  5799  5799 W .ghprotocol.app: type=1400 audit(0.0:47): avc:  granted  { execute } for  name="Xray" dev="dm-40" ino=132102 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c192,c256,c512,c768 tclass=file app=com.ghprotocol.app
10-25 05:43:21.294  5799  5799 W .ghprotocol.app: type=1400 audit(0.0:48): avc:  denied  { execute_no_trans } for  path="/data/data/com.ghprotocol.app/files/xray/Xray" dev="dm-40" ino=132102 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c192,c256,c512,c768 tclass=file permissive=0 app=com.ghprotocol.app
10-25 05:43:21.319   526  2280 D CoreBackPreview: Window{57ce17b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@98e8ff1, mPriority=0, mIsAnimationCallback=false}
10-25 05:43:21.408   830   870 V WindowManagerShell: onTransitionReady android.os.BinderProxy@1df6539: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity)/@0x521952c sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity)/@0x6c81bf5 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:43:21.409   830   870 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity)/@0x521952c sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity)/@0x6c81bf5 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:43:21.412   526   543 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +500ms
10-25 05:43:21.413   526   543 V WindowManager: Sent Transition #7 createdAt=10-25 05:43:20.903 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=97702 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{7b4e7fd Task{bfb3224 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{6d004f3 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:43:21.413   526   543 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity)/@0xfeb3a2d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity)/@0x331e944 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:43:21.414   830   870 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{260be5f u0 com.ghprotocol.app/.MainActivity)/@0x521952c sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{19d7ab7 u0 com.ghprotocol.app/.MainActivity)/@0x6c81bf5 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:43:21.608   526  2208 I ImeTracker: com.ghprotocol.app:5c2e172a: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 05:43:21.608   526  2208 I ImeTracker: com.ghprotocol.app:5c2e172a: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 05:43:21.613  1522  1522 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 05:43:29.149  5829  5829 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:43:29.152  5829  5829 I AndroidRuntime: Using default boot image
10-25 05:43:29.152  5829  5829 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:43:29.256  5829  5829 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:43:30.342  5829  5829 D AndroidRuntime: Shutting down VM
10-25 05:43:31.760   526   577 I AppsFilter: interaction: PackageSetting{94fad35 com.ghprotocol.app/10192} -> PackageSetting{710ff26 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 05:43:43.365  5888  5888 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:43:43.371  5888  5888 I AndroidRuntime: Using default boot image
10-25 05:43:43.371  5888  5888 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:43:43.446  5888  5888 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:43:44.488  5888  5888 D AndroidRuntime: Shutting down VM
10-25 05:43:57.530  5971  5971 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:43:57.533  5971  5971 I AndroidRuntime: Using default boot image
10-25 05:43:57.533  5971  5971 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:43:57.594  5971  5971 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:43:58.644  5971  5971 D AndroidRuntime: Shutting down VM
10-25 05:43:59.752   526   577 I AppsFilter: interaction: PackageSetting{94fad35 com.ghprotocol.app/10192} -> PackageSetting{5a10ea3 com.google.android.contacts/10154} BLOCKED
10-25 05:44:09.768   526   577 I AppsFilter: interaction: PackageSetting{94fad35 com.ghprotocol.app/10192} -> PackageSetting{7ca5e8 com.google.android.contacts/10154} BLOCKED
10-25 05:44:11.664  6020  6020 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:44:11.667  6020  6020 I AndroidRuntime: Using default boot image
10-25 05:44:11.667  6020  6020 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:44:11.726  6020  6020 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:44:12.760  6020  6020 D AndroidRuntime: Shutting down VM
10-25 05:44:25.761  6058  6058 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:44:25.763  6058  6058 I AndroidRuntime: Using default boot image
10-25 05:44:25.763  6058  6058 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:44:25.819  6058  6058 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:44:26.854  6058  6058 D AndroidRuntime: Shutting down VM
10-25 05:44:39.950  6106  6106 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:44:39.952  6106  6106 I AndroidRuntime: Using default boot image
10-25 05:44:39.952  6106  6106 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:44:40.010  6106  6106 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:44:41.043  6106  6106 D AndroidRuntime: Shutting down VM
10-25 05:44:54.073  6146  6146 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:44:54.076  6146  6146 I AndroidRuntime: Using default boot image
10-25 05:44:54.076  6146  6146 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:44:54.134  6146  6146 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:44:55.171  6146  6146 D AndroidRuntime: Shutting down VM
10-25 05:45:08.151  6190  6190 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:45:08.153  6190  6190 I AndroidRuntime: Using default boot image
10-25 05:45:08.153  6190  6190 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:45:08.211  6190  6190 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:45:09.248  6190  6190 D AndroidRuntime: Shutting down VM
10-25 05:45:22.265  6216  6216 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:45:22.268  6216  6216 I AndroidRuntime: Using default boot image
10-25 05:45:22.268  6216  6216 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:45:22.323  6216  6216 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:45:23.354  6216  6216 D AndroidRuntime: Shutting down VM
10-25 05:45:36.349  6246  6246 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:45:36.352  6246  6246 I AndroidRuntime: Using default boot image
10-25 05:45:36.352  6246  6246 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:45:36.412  6246  6246 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:45:37.444  6246  6246 D AndroidRuntime: Shutting down VM
10-25 05:45:50.430  6271  6271 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:45:50.433  6271  6271 I AndroidRuntime: Using default boot image
10-25 05:45:50.433  6271  6271 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:45:50.489  6271  6271 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:45:51.545  6271  6271 D AndroidRuntime: Shutting down VM
10-25 05:46:04.523  6306  6306 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:46:04.526  6306  6306 I AndroidRuntime: Using default boot image
10-25 05:46:04.526  6306  6306 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:46:04.582  6306  6306 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:46:05.619  6306  6306 D AndroidRuntime: Shutting down VM
10-25 05:46:18.611  6331  6331 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:46:18.613  6331  6331 I AndroidRuntime: Using default boot image
10-25 05:46:18.613  6331  6331 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:46:18.669  6331  6331 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:46:19.728  6331  6331 D AndroidRuntime: Shutting down VM
10-25 05:46:32.719  6358  6358 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:46:32.722  6358  6358 I AndroidRuntime: Using default boot image
10-25 05:46:32.722  6358  6358 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:46:32.779  6358  6358 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:46:33.806  6358  6358 D AndroidRuntime: Shutting down VM
10-25 05:46:46.806  6402  6402 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:46:46.809  6402  6402 I AndroidRuntime: Using default boot image
10-25 05:46:46.809  6402  6402 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:46:46.866  6402  6402 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:46:47.900  6402  6402 D AndroidRuntime: Shutting down VM
10-25 05:47:00.889  6431  6431 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:47:00.892  6431  6431 I AndroidRuntime: Using default boot image
10-25 05:47:00.892  6431  6431 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:47:00.950  6431  6431 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:47:01.981  6431  6431 D AndroidRuntime: Shutting down VM
10-25 05:47:14.988  6463  6463 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:47:14.990  6463  6463 I AndroidRuntime: Using default boot image
10-25 05:47:14.990  6463  6463 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:47:15.045  6463  6463 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:47:16.083  6463  6463 D AndroidRuntime: Shutting down VM
10-25 05:47:29.063  6518  6518 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:47:29.065  6518  6518 I AndroidRuntime: Using default boot image
10-25 05:47:29.065  6518  6518 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:47:29.122  6518  6518 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:47:30.152  6518  6518 D AndroidRuntime: Shutting down VM
10-25 05:47:43.138  6547  6547 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:47:43.141  6547  6547 I AndroidRuntime: Using default boot image
10-25 05:47:43.141  6547  6547 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:47:43.199  6547  6547 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:47:44.236  6547  6547 D AndroidRuntime: Shutting down VM
10-25 05:47:57.223  6575  6575 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:47:57.225  6575  6575 I AndroidRuntime: Using default boot image
10-25 05:47:57.225  6575  6575 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:47:57.283  6575  6575 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:47:58.314  6575  6575 D AndroidRuntime: Shutting down VM
10-25 05:48:11.289  6626  6626 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:48:11.292  6626  6626 I AndroidRuntime: Using default boot image
10-25 05:48:11.292  6626  6626 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:48:11.347  6626  6626 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:48:12.377  6626  6626 D AndroidRuntime: Shutting down VM
10-25 05:48:25.407  6659  6659 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:48:25.409  6659  6659 I AndroidRuntime: Using default boot image
10-25 05:48:25.409  6659  6659 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:48:25.466  6659  6659 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:48:26.500  6659  6659 D AndroidRuntime: Shutting down VM
10-25 05:48:39.472  6685  6685 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:48:39.475  6685  6685 I AndroidRuntime: Using default boot image
10-25 05:48:39.475  6685  6685 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:48:39.531  6685  6685 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:48:40.576  6685  6685 D AndroidRuntime: Shutting down VM
10-25 05:48:53.550  6714  6714 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:48:53.552  6714  6714 I AndroidRuntime: Using default boot image
10-25 05:48:53.552  6714  6714 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:48:53.612  6714  6714 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:48:54.652  6714  6714 D AndroidRuntime: Shutting down VM
10-25 05:49:07.629  6744  6744 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:49:07.632  6744  6744 I AndroidRuntime: Using default boot image
10-25 05:49:07.632  6744  6744 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:49:07.693  6744  6744 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:49:08.737  6744  6744 D AndroidRuntime: Shutting down VM
10-25 05:49:21.718  6769  6769 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:49:21.720  6769  6769 I AndroidRuntime: Using default boot image
10-25 05:49:21.721  6769  6769 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:49:21.778  6769  6769 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:49:22.807  6769  6769 D AndroidRuntime: Shutting down VM
10-25 05:49:35.831  6799  6799 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:49:35.834  6799  6799 I AndroidRuntime: Using default boot image
10-25 05:49:35.834  6799  6799 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:49:35.894  6799  6799 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:49:36.932  6799  6799 D AndroidRuntime: Shutting down VM
10-25 05:49:49.912  6823  6823 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:49:49.915  6823  6823 I AndroidRuntime: Using default boot image
10-25 05:49:49.915  6823  6823 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:49:49.988  6823  6823 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:49:51.020  6823  6823 D AndroidRuntime: Shutting down VM
10-25 05:50:04.010  6849  6849 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:50:04.013  6849  6849 I AndroidRuntime: Using default boot image
10-25 05:50:04.013  6849  6849 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:50:04.073  6849  6849 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:50:05.108  6849  6849 D AndroidRuntime: Shutting down VM
10-25 05:50:18.107  6874  6874 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:50:18.110  6874  6874 I AndroidRuntime: Using default boot image
10-25 05:50:18.110  6874  6874 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:50:18.170  6874  6874 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:50:19.207  6874  6874 D AndroidRuntime: Shutting down VM


