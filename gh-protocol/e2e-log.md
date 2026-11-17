## gh-protocol E2E log — 2026-11-17T15:17:05Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-11-17T15:06:45Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Nov 17 15:03 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Nov 17 15:07 .
drwxr-xr-x 3 runner runner 4096 Nov 17 15:07 ..
drwxr-xr-x 3 runner runner 4096 Nov 17 15:07 gh_test.avd
-rw-r--r-- 1 runner runner  115 Nov 17 15:07 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.13.0 (build_id 16740729) (CL:N/A)
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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15700 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15700 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 3230
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
INFO         |   androidboot.serialno=EMULATOR37X2X13X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7819d6401000 as it is in the protected range from 0x7818d6400000 to 0x7819d6600000
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
INFO         | Boot completed in 32629 ms
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
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
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
> Task :app:mergeDebugAssets
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
e: The daemon has terminated unexpectedly on startup attempt #1 with error code: 0. The daemon process output:
    1. Kotlin compile daemon is ready
e: The daemon has terminated unexpectedly on startup attempt #2 with error code: 0. The daemon process output:
    1. Kotlin compile daemon is ready
Problems may have occurred during auto-selection of GC. The preferred GC is Parallel GC.
If the problems persist, try adding the JVM option to the Kotlin daemon JVM arguments: -XX:-UseParallelGC.
GC auto-selection logic is disabled temporary for the next daemon startup.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:608:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1794927854450.json

BUILD SUCCESSFUL in 2m 15s
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
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2916)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       2916   337   13936464 185368 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp      130      0 10.0.2.16:38536         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:59664         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:45734         142.251.151.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:34726         142.251.151.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:38514         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:38484         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:38522         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:51694         172.217.116.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:53044         172.217.115.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:38504         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:38492         172.217.118.4:443       CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:36095  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:37265  [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:56250  ::ffff:142.251.163.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:53060  ::ffff:172.217.115.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:56134  ::ffff:142.251.167.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:46922  ::ffff:192.178.155.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:41390  ::ffff:142.251.156.:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.16:55588  ::ffff:142.251.163:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:53058  ::ffff:172.217.115.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{29f2489 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{29bd35f 2916:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~24MD4LiXfPeaH0ze1QhMUA==/com.ghprotocol.app-oiQVYvC9WmHJUnxz-g77sw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-9m10s27ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{29f2489 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{29bd35f 2916:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~24MD4LiXfPeaH0ze1QhMUA==/com.ghprotocol.app-oiQVYvC9WmHJUnxz-g77sw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.2 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{8ee69 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-9m15s94ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@90856028
  deepestLastOrientationSource=ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=92
  mCurrentFocus=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{29f2489 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{d0e7e3a #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{b524614 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{6b5a867 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{cc95627 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{2f1e27d #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{f8f33cf u0 StatusBar}
    mFocusedWindow=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{e695f7a u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=f560006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {f560000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=f560006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{f8f33cf u0 StatusBar}
--
        mWindowContainer=Window{f8f33cf u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=f8f33cf StatusBar)/@0x24fbba7 - animation-leash of insets_animation)/@0x290ba16
        mControlTarget=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=1c0ebd6 InputMethod)/@0x9366029 - animation-leash of insets_animation)/@0x3561f97 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{1c0ebd6 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=1c0ebd6 InputMethod)/@0x9366029 - animation-leash of insets_animation)/@0x3561f97
        mControlTarget=Window{5d352eb u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{323c0d4 #3 type=undefined}
        (multi-window) Task{2f1e27d #4 type=undefined}
        (fullscreen) Task{5da7c8e #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{29bd35f 2916:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10164:1]
app filesDir/xray (geo data):
total 6212
drwx------ 2 u0_a192 u0_a192    4096 2026-11-17 15:07 .
drwxrwx--x 3 u0_a192 u0_a192    4096 2026-11-17 15:07 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-11-17 15:07 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-11-17 15:07 geosite.dat
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
runtime config (first 1400 bytes):
core exit line:
GhDiag (connect-flow trace):
--------- beginning of main
11-17 15:07:53.141  2916  2916 D GhDiag  : connect: tap -> CHECKING (have sub=true)
11-17 15:07:53.141  2916  2916 D GhDiag  : connect: sub ok entries=3 -> PREPARING (core extract+version)
11-17 15:07:53.477  2916  2916 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
11-17 15:07:53.478  2916  2916 D GhDiag  : connect: FAILED — core unavailable/old (min=26.11.21)
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
d 2000 <<<<<<
11-17 15:10:15.581  6202  6202 I AndroidRuntime: Using default boot image
11-17 15:10:15.581  6202  6202 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:15.661  6202  6202 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:16.715  6202  6202 D AndroidRuntime: Shutting down VM
11-17 15:10:21.660  6227  6227 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:21.663  6227  6227 I AndroidRuntime: Using default boot image
11-17 15:10:21.663  6227  6227 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:21.744  6227  6227 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:22.801  6227  6227 D AndroidRuntime: Shutting down VM
11-17 15:10:27.765  6252  6252 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:27.769  6252  6252 I AndroidRuntime: Using default boot image
11-17 15:10:27.769  6252  6252 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:27.856  6252  6252 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:28.908  6252  6252 D AndroidRuntime: Shutting down VM
11-17 15:10:33.860  6284  6284 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:33.863  6284  6284 I AndroidRuntime: Using default boot image
11-17 15:10:33.863  6284  6284 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:33.944  6284  6284 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:35.009  6284  6284 D AndroidRuntime: Shutting down VM
11-17 15:10:39.976  6314  6314 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:39.980  6314  6314 I AndroidRuntime: Using default boot image
11-17 15:10:39.980  6314  6314 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:40.062  6314  6314 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:41.122  6314  6314 D AndroidRuntime: Shutting down VM
11-17 15:10:46.074  6338  6338 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:46.078  6338  6338 I AndroidRuntime: Using default boot image
11-17 15:10:46.078  6338  6338 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:46.163  6338  6338 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:47.224  6338  6338 D AndroidRuntime: Shutting down VM
11-17 15:10:52.178  6364  6364 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:52.181  6364  6364 I AndroidRuntime: Using default boot image
11-17 15:10:52.181  6364  6364 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:52.261  6364  6364 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:53.302  6364  6364 D AndroidRuntime: Shutting down VM
11-17 15:10:58.280  6389  6389 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:10:58.283  6389  6389 I AndroidRuntime: Using default boot image
11-17 15:10:58.283  6389  6389 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:10:58.365  6389  6389 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:10:59.421  6389  6389 D AndroidRuntime: Shutting down VM
11-17 15:11:04.385  6412  6412 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:04.388  6412  6412 I AndroidRuntime: Using default boot image
11-17 15:11:04.388  6412  6412 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:04.470  6412  6412 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:05.531  6412  6412 D AndroidRuntime: Shutting down VM
11-17 15:11:10.481  6436  6436 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:10.484  6436  6436 I AndroidRuntime: Using default boot image
11-17 15:11:10.484  6436  6436 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:10.567  6436  6436 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:11.619  6436  6436 D AndroidRuntime: Shutting down VM
11-17 15:11:16.578  6459  6459 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:16.582  6459  6459 I AndroidRuntime: Using default boot image
11-17 15:11:16.582  6459  6459 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:16.662  6459  6459 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:17.719  6459  6459 D AndroidRuntime: Shutting down VM
11-17 15:11:22.665  6484  6484 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:22.669  6484  6484 I AndroidRuntime: Using default boot image
11-17 15:11:22.669  6484  6484 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:22.749  6484  6484 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:23.808  6484  6484 D AndroidRuntime: Shutting down VM
11-17 15:11:28.775  6509  6509 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:28.778  6509  6509 I AndroidRuntime: Using default boot image
11-17 15:11:28.779  6509  6509 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:28.860  6509  6509 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:29.907  6509  6509 D AndroidRuntime: Shutting down VM
11-17 15:11:34.852  6533  6533 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:34.855  6533  6533 I AndroidRuntime: Using default boot image
11-17 15:11:34.855  6533  6533 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:34.936  6533  6533 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:36.001  6533  6533 D AndroidRuntime: Shutting down VM
11-17 15:11:40.961  6557  6557 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:40.964  6557  6557 I AndroidRuntime: Using default boot image
11-17 15:11:40.964  6557  6557 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:41.047  6557  6557 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:42.100  6557  6557 D AndroidRuntime: Shutting down VM
11-17 15:11:47.052  6580  6580 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:47.056  6580  6580 I AndroidRuntime: Using default boot image
11-17 15:11:47.056  6580  6580 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:47.138  6580  6580 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:48.185  6580  6580 D AndroidRuntime: Shutting down VM
11-17 15:11:53.152  6605  6605 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:53.155  6605  6605 I AndroidRuntime: Using default boot image
11-17 15:11:53.155  6605  6605 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:53.238  6605  6605 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:11:54.290  6605  6605 D AndroidRuntime: Shutting down VM
11-17 15:11:59.264  6630  6630 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:11:59.268  6630  6630 I AndroidRuntime: Using default boot image
11-17 15:11:59.268  6630  6630 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:11:59.350  6630  6630 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:00.415  6630  6630 D AndroidRuntime: Shutting down VM
11-17 15:12:05.364  6655  6655 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:05.368  6655  6655 I AndroidRuntime: Using default boot image
11-17 15:12:05.368  6655  6655 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:05.448  6655  6655 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:06.506  6655  6655 D AndroidRuntime: Shutting down VM
11-17 15:12:11.467  6678  6678 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:11.471  6678  6678 I AndroidRuntime: Using default boot image
11-17 15:12:11.471  6678  6678 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:11.554  6678  6678 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:12.607  6678  6678 D AndroidRuntime: Shutting down VM
11-17 15:12:17.568  6705  6705 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:17.572  6705  6705 I AndroidRuntime: Using default boot image
11-17 15:12:17.572  6705  6705 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:17.650  6705  6705 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:18.713  6705  6705 D AndroidRuntime: Shutting down VM
11-17 15:12:23.663  6729  6729 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:23.666  6729  6729 I AndroidRuntime: Using default boot image
11-17 15:12:23.666  6729  6729 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:23.744  6729  6729 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:24.786  6729  6729 D AndroidRuntime: Shutting down VM
11-17 15:12:29.745  6754  6754 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:29.749  6754  6754 I AndroidRuntime: Using default boot image
11-17 15:12:29.749  6754  6754 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:29.832  6754  6754 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:30.888  6754  6754 D AndroidRuntime: Shutting down VM
11-17 15:12:35.842  6812  6812 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:35.845  6812  6812 I AndroidRuntime: Using default boot image
11-17 15:12:35.845  6812  6812 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:35.925  6812  6812 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:36.976  6812  6812 D AndroidRuntime: Shutting down VM
11-17 15:12:41.929  6842  6842 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:41.932  6842  6842 I AndroidRuntime: Using default boot image
11-17 15:12:41.932  6842  6842 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:42.014  6842  6842 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:43.056  6842  6842 D AndroidRuntime: Shutting down VM
11-17 15:12:48.014  6865  6865 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:48.018  6865  6865 I AndroidRuntime: Using default boot image
11-17 15:12:48.018  6865  6865 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:48.098  6865  6865 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:49.157  6865  6865 D AndroidRuntime: Shutting down VM
11-17 15:12:54.146  6888  6888 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:12:54.150  6888  6888 I AndroidRuntime: Using default boot image
11-17 15:12:54.150  6888  6888 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:12:54.231  6888  6888 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:12:55.274  6888  6888 D AndroidRuntime: Shutting down VM
11-17 15:13:00.243  6914  6914 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:00.246  6914  6914 I AndroidRuntime: Using default boot image
11-17 15:13:00.246  6914  6914 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:00.331  6914  6914 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:01.388  6914  6914 D AndroidRuntime: Shutting down VM
11-17 15:13:06.336  6937  6937 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:06.340  6937  6937 I AndroidRuntime: Using default boot image
11-17 15:13:06.340  6937  6937 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:06.420  6937  6937 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:07.484  6937  6937 D AndroidRuntime: Shutting down VM
11-17 15:13:12.438  6962  6962 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:12.441  6962  6962 I AndroidRuntime: Using default boot image
11-17 15:13:12.441  6962  6962 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:12.523  6962  6962 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:13.566  6962  6962 D AndroidRuntime: Shutting down VM
11-17 15:13:18.529  6987  6987 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:18.532  6987  6987 I AndroidRuntime: Using default boot image
11-17 15:13:18.532  6987  6987 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:18.615  6987  6987 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:19.655  6987  6987 D AndroidRuntime: Shutting down VM
11-17 15:13:24.611  7109  7109 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:24.614  7109  7109 I AndroidRuntime: Using default boot image
11-17 15:13:24.614  7109  7109 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:24.709  7109  7109 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:25.742  7109  7109 D AndroidRuntime: Shutting down VM
11-17 15:13:27.389   522   574 I AppsFilter: interaction: PackageSetting{3fe73ac com.ghprotocol.app/10192} -> PackageSetting{76f4258 com.google.android.contacts/10154} BLOCKED
11-17 15:13:30.733  7151  7151 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:30.736  7151  7151 I AndroidRuntime: Using default boot image
11-17 15:13:30.736  7151  7151 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:30.817  7151  7151 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:31.880  7151  7151 D AndroidRuntime: Shutting down VM
11-17 15:13:36.829  7175  7175 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:36.833  7175  7175 I AndroidRuntime: Using default boot image
11-17 15:13:36.833  7175  7175 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:36.911  7175  7175 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:37.401   522   574 I AppsFilter: interaction: PackageSetting{3fe73ac com.ghprotocol.app/10192} -> PackageSetting{27d72d9 com.google.android.contacts/10154} BLOCKED
11-17 15:13:37.971  7175  7175 D AndroidRuntime: Shutting down VM
11-17 15:13:42.929  7210  7210 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:42.932  7210  7210 I AndroidRuntime: Using default boot image
11-17 15:13:42.932  7210  7210 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:43.014  7210  7210 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:44.063  7210  7210 D AndroidRuntime: Shutting down VM
11-17 15:13:49.011  7240  7240 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:49.014  7240  7240 I AndroidRuntime: Using default boot image
11-17 15:13:49.014  7240  7240 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:49.096  7240  7240 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:50.151  7240  7240 D AndroidRuntime: Shutting down VM
11-17 15:13:55.098  7263  7263 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:13:55.102  7263  7263 I AndroidRuntime: Using default boot image
11-17 15:13:55.102  7263  7263 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:13:55.183  7263  7263 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:13:56.240  7263  7263 D AndroidRuntime: Shutting down VM
11-17 15:14:01.259  7289  7289 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:01.262  7289  7289 I AndroidRuntime: Using default boot image
11-17 15:14:01.262  7289  7289 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:01.343  7289  7289 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:02.393  7289  7289 D AndroidRuntime: Shutting down VM
11-17 15:14:07.344  7312  7312 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:07.347  7312  7312 I AndroidRuntime: Using default boot image
11-17 15:14:07.347  7312  7312 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:07.428  7312  7312 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:08.473  7312  7312 D AndroidRuntime: Shutting down VM
11-17 15:14:13.416  7337  7337 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:13.420  7337  7337 I AndroidRuntime: Using default boot image
11-17 15:14:13.420  7337  7337 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:13.499  7337  7337 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:14.547  7337  7337 D AndroidRuntime: Shutting down VM
11-17 15:14:19.502  7367  7367 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:19.506  7367  7367 I AndroidRuntime: Using default boot image
11-17 15:14:19.506  7367  7367 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:19.587  7367  7367 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:20.640  7367  7367 D AndroidRuntime: Shutting down VM
11-17 15:14:25.591  7390  7390 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:25.595  7390  7390 I AndroidRuntime: Using default boot image
11-17 15:14:25.595  7390  7390 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:25.676  7390  7390 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:26.720  7390  7390 D AndroidRuntime: Shutting down VM
11-17 15:14:31.678  7415  7415 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:31.682  7415  7415 I AndroidRuntime: Using default boot image
11-17 15:14:31.682  7415  7415 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:31.762  7415  7415 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:32.818  7415  7415 D AndroidRuntime: Shutting down VM
11-17 15:14:37.764  7438  7438 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:37.768  7438  7438 I AndroidRuntime: Using default boot image
11-17 15:14:37.768  7438  7438 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:37.849  7438  7438 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:38.897  7438  7438 D AndroidRuntime: Shutting down VM
11-17 15:14:43.844  7462  7462 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:43.848  7462  7462 I AndroidRuntime: Using default boot image
11-17 15:14:43.848  7462  7462 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:43.931  7462  7462 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:44.988  7462  7462 D AndroidRuntime: Shutting down VM
11-17 15:14:49.931  7485  7485 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:49.934  7485  7485 I AndroidRuntime: Using default boot image
11-17 15:14:49.934  7485  7485 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:50.015  7485  7485 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:51.079  7485  7485 D AndroidRuntime: Shutting down VM
11-17 15:14:56.026  7508  7508 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:14:56.030  7508  7508 I AndroidRuntime: Using default boot image
11-17 15:14:56.030  7508  7508 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:14:56.109  7508  7508 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:14:57.169  7508  7508 D AndroidRuntime: Shutting down VM
11-17 15:15:02.131  7533  7533 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:02.135  7533  7533 I AndroidRuntime: Using default boot image
11-17 15:15:02.135  7533  7533 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:02.218  7533  7533 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:03.288  7533  7533 D AndroidRuntime: Shutting down VM
11-17 15:15:08.247  7558  7558 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:08.251  7558  7558 I AndroidRuntime: Using default boot image
11-17 15:15:08.251  7558  7558 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:08.333  7558  7558 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:09.382  7558  7558 D AndroidRuntime: Shutting down VM
11-17 15:15:14.333  7591  7591 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:14.337  7591  7591 I AndroidRuntime: Using default boot image
11-17 15:15:14.337  7591  7591 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:14.419  7591  7591 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:15.484  7591  7591 D AndroidRuntime: Shutting down VM
11-17 15:15:20.449  7613  7613 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:20.453  7613  7613 I AndroidRuntime: Using default boot image
11-17 15:15:20.453  7613  7613 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:20.541  7613  7613 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:21.607  7613  7613 D AndroidRuntime: Shutting down VM
11-17 15:15:26.584  7637  7637 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:26.588  7637  7637 I AndroidRuntime: Using default boot image
11-17 15:15:26.588  7637  7637 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:26.674  7637  7637 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:27.707  7637  7637 D AndroidRuntime: Shutting down VM
11-17 15:15:32.679  7669  7669 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:32.683  7669  7669 I AndroidRuntime: Using default boot image
11-17 15:15:32.683  7669  7669 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:32.767  7669  7669 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:33.810  7669  7669 D AndroidRuntime: Shutting down VM
11-17 15:15:38.766  7692  7692 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:38.769  7692  7692 I AndroidRuntime: Using default boot image
11-17 15:15:38.769  7692  7692 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:38.851  7692  7692 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:39.906  7692  7692 D AndroidRuntime: Shutting down VM
11-17 15:15:44.876  7716  7716 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:44.880  7716  7716 I AndroidRuntime: Using default boot image
11-17 15:15:44.880  7716  7716 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:44.963  7716  7716 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:46.021  7716  7716 D AndroidRuntime: Shutting down VM
11-17 15:15:50.978  7740  7740 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:50.981  7740  7740 I AndroidRuntime: Using default boot image
11-17 15:15:50.981  7740  7740 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:51.065  7740  7740 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:52.120  7740  7740 D AndroidRuntime: Shutting down VM
11-17 15:15:57.074  7764  7764 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:15:57.077  7764  7764 I AndroidRuntime: Using default boot image
11-17 15:15:57.077  7764  7764 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:15:57.163  7764  7764 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:15:58.223  7764  7764 D AndroidRuntime: Shutting down VM
11-17 15:16:03.204  7789  7789 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:03.208  7789  7789 I AndroidRuntime: Using default boot image
11-17 15:16:03.208  7789  7789 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:03.290  7789  7789 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:04.341  7789  7789 D AndroidRuntime: Shutting down VM
11-17 15:16:09.300  7812  7812 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:09.304  7812  7812 I AndroidRuntime: Using default boot image
11-17 15:16:09.304  7812  7812 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:09.385  7812  7812 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:10.433  7812  7812 D AndroidRuntime: Shutting down VM
11-17 15:16:15.383  7835  7835 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:15.386  7835  7835 I AndroidRuntime: Using default boot image
11-17 15:16:15.386  7835  7835 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:15.467  7835  7835 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:16.545  7835  7835 D AndroidRuntime: Shutting down VM
11-17 15:16:21.494  7860  7860 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:21.498  7860  7860 I AndroidRuntime: Using default boot image
11-17 15:16:21.498  7860  7860 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:21.579  7860  7860 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:22.638  7860  7860 D AndroidRuntime: Shutting down VM
11-17 15:16:27.592  7883  7883 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:27.595  7883  7883 I AndroidRuntime: Using default boot image
11-17 15:16:27.596  7883  7883 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:27.676  7883  7883 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:28.725  7883  7883 D AndroidRuntime: Shutting down VM
11-17 15:16:33.691  7908  7908 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:33.694  7908  7908 I AndroidRuntime: Using default boot image
11-17 15:16:33.694  7908  7908 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:33.773  7908  7908 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:34.806  7908  7908 D AndroidRuntime: Shutting down VM
11-17 15:16:39.773  7931  7931 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:39.776  7931  7931 I AndroidRuntime: Using default boot image
11-17 15:16:39.776  7931  7931 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:39.858  7931  7931 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:40.896  7931  7931 D AndroidRuntime: Shutting down VM
11-17 15:16:45.836  7954  7954 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:45.839  7954  7954 I AndroidRuntime: Using default boot image
11-17 15:16:45.839  7954  7954 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:45.918  7954  7954 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:46.976  7954  7954 D AndroidRuntime: Shutting down VM
11-17 15:16:51.919  7977  7977 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:51.922  7977  7977 I AndroidRuntime: Using default boot image
11-17 15:16:51.922  7977  7977 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:52.003  7977  7977 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:53.045  7977  7977 D AndroidRuntime: Shutting down VM
11-17 15:16:57.988  8000  8000 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 15:16:57.992  8000  8000 I AndroidRuntime: Using default boot image
11-17 15:16:57.992  8000  8000 I AndroidRuntime: Leaving lock profiling enabled
11-17 15:16:58.071  8000  8000 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 15:16:59.118  8000  8000 D AndroidRuntime: Shutting down VM


