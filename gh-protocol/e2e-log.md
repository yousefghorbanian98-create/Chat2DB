## gh-protocol E2E log — 2026-10-25T06:13:48Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T06:05:01Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 06:01 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 06:05 .
drwxr-xr-x 3 runner runner 4096 Oct 25 06:05 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 06:05 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 06:05 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3070
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
WARNING: cannnot unmap ptr 0x7f2d68201000 as it is in the protected range from 0x7f2c68200000 to 0x7f2d68400000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 38543 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 177
ERROR        | Failed to bind to texture: invalid color buffer.

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
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:validateSigningDebug
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:compileDebugKotlin
e: The daemon has terminated unexpectedly on startup attempt #1 with error code: 0. The daemon process output:
    1. Kotlin compile daemon is ready
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792908142211.json

BUILD SUCCESSFUL in 2m 33s
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
seeded cache: 37417 bytes, meta=1792908443075
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5509)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5509   336   13899424 172408 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:44223  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:45227  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:55904  ::ffff:142.251.157.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{365d3f3 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a961906 5509:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~4At_lcVazaelmYlod-9_tw==/com.ghprotocol.app-BE2r9Cg5yBo5cZGibbU0DA==/base.apk
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
      windows=[Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m14s296ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{20df22e u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a961906 5509:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~4At_lcVazaelmYlod-9_tw==/com.ghprotocol.app-BE2r9Cg5yBo5cZGibbU0DA==/base.apk
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
      windows=[Window{7dd2d4d u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m21s30ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@146408318
  deepestLastOrientationSource=ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=96
  mCurrentFocus=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{20df22e u0 com.ghprotocol.app/.MainActivity t8}
      * Task{ffd512c #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{55aa2da #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{8420485 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{c0aa286 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{ec95b74 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{5ceb60a u0 StatusBar}
    mFocusedWindow=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{f842f02 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
    Control map:
      Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {cc320000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=e761c20 InputMethod)/@0x8cd8a7f - animation-leash of insets_animation)/@0xf8d5b63 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{e761c20 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=e761c20 InputMethod)/@0x8cd8a7f - animation-leash of insets_animation)/@0xf8d5b63
        mControlTarget=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false
      InsetsSourceProvider
        mSource=InsetsSource id=cc320006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{5ceb60a u0 StatusBar}
      InsetsSourceProvider
        mSource=InsetsSource id=cc320005 type=mandatorySystemGestures frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
--
        mWindowContainer=Window{5ceb60a u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=5ceb60a StatusBar)/@0xe703c6b - animation-leash of insets_animation)/@0x29a4360
        mControlTarget=Window{5f8dc49 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false

--
        (multi-window) Task{7b03747 #3 type=undefined}
        (multi-window) Task{ec95b74 #4 type=undefined}
        (fullscreen) Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{a961906 5509:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6216
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 06:07 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 06:07 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 06:07 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 06:07 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 06:07 xray-err.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-25 06:07:31.380  5509  5509 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:07:31.381  5509  5509 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:07:31.604  5509  5509 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:07:31.625  5509  5509 D GhDiag  : connect: config written bytes=5564 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:07:31.752  5509  5509 D GhDiag  : connect: core.start=true 
10-25 06:07:42.305  5509  5509 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:07:42.358  5509  5509 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@def4631} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
nt=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=120713 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@df2d62c} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{faec8f5 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:07:32.343   524  2021 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 06:07:32.372   524  1866 I ImeTracker: com.ghprotocol.app:7a68a307: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 06:07:32.372   524  1866 I ImeTracker: com.ghprotocol.app:7a68a307: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:07:32.377   524  2021 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 06:07:32.377   524  2021 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 06:07:32.393  1544  1544 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:07:33.262   524   541 V WindowManager: Sent Transition #8 createdAt=10-25 06:07:32.031 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=120713 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{14aaeea Task{d4e51cf #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{eb0f615 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:07:33.403   524   576 I AppsFilter: interaction: PackageSetting{72a801c com.ghprotocol.app/10192} -> PackageSetting{4b7de91 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 06:07:33.403   524   576 I AppsFilter: interaction: PackageSetting{72a801c com.ghprotocol.app/10192} -> PackageSetting{d4021f6 com.google.android.contacts/10155} BLOCKED
10-25 06:07:33.480  5509  5518 I .ghprotocol.app: Background concurrent copying GC freed 97774(5047KB) AllocSpace objects, 30(896KB) LOS objects, 49% free, 6475KB/12MB, paused 43us,9us total 292.782ms
10-25 06:07:39.953  5777  5777 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 06:07:39.960  5777  5777 I AndroidRuntime: Using default boot image
10-25 06:07:39.960  5777  5777 I AndroidRuntime: Leaving lock profiling enabled
10-25 06:07:40.053  5777  5777 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 06:07:41.093  5777  5777 D AndroidRuntime: Shutting down VM
10-25 06:07:42.152   524   537 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 06:07:42.292   524  2346 I ImeTracker: com.ghprotocol.app:b5e0a320: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 06:07:42.302   524  2346 I ImeTracker: com.ghprotocol.app:b5e0a320: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:07:42.305  5509  5509 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:07:42.346  1544  1544 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:07:42.358   524  2346 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 06:07:42.358  5509  5509 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@def4631} — relay loop started
10-25 06:07:42.549  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33340) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:42.756  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33350) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:43.164  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33364) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:43.676  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33368) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:43.996  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33374) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:44.700  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33388) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:45.660  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33402) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:46.716  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33418) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:49.052  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33428) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:50.844  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33442) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:55.708  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 35378) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:07:59.036  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 35384) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:08:09.020  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34444) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:08:17.274   524   576 I AppsFilter: interaction: PackageSetting{72a801c com.ghprotocol.app/10192} -> PackageSetting{c7b0d71 com.google.android.contacts/10155} BLOCKED
10-25 06:08:27.283   524   576 I AppsFilter: interaction: PackageSetting{72a801c com.ghprotocol.app/10192} -> PackageSetting{86471d7 com.google.android.contacts/10155} BLOCKED
10-25 06:08:36.667  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52116) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:09:32.335  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:09:32.339  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.475  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.475  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.609  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.609  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.736  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.736  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.858  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.858  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.973  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:32.973  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.083  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.083  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.187  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.187  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.285  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.285  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.456  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.456  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.544  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.544  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.626  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.626  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.701  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.701  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.770  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.770  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.832  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.832  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.887  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.887  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.937  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.937  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.982  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:33.982  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.020  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.020  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.052  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.052  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.079  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.079  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.099  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.099  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.113  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.113  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.122  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.122  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.125  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.125  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.125  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:09:34.128  5509  5520 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 06:09:34.128  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.128  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.128  5509  5520 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:09:34.139  5509  5805 I .ghprotocol.app: Alloc concurrent copying GC freed 5262(212KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 6268KB/12MB, paused 14us,3us total 10.563ms
10-25 06:09:34.139  5509  5520 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 10.931ms
10-25 06:09:34.139  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:09:34.149  5509  5520 I .ghprotocol.app: Alloc concurrent copying GC freed 4435(176KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6476KB/12MB, paused 44us,8us total 9.887ms
10-25 06:11:28.284  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:11:28.287  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.434  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.434  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.577  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.577  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.714  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.714  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.846  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.846  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.971  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:28.971  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.092  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.092  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.208  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.208  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.349  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.349  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.357  5509  5805 I .ghprotocol.app: Alloc young concurrent copying GC freed 52412(4623KB) AllocSpace objects, 0(0B) LOS objects, 51% free, 6278KB/12MB, paused 33us,4us total 7.596ms
10-25 06:11:29.500  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.500  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.596  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.597  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.687  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.687  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.772  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.772  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.851  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.851  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.923  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.923  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.990  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:29.990  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.051  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.051  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.111  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.111  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.161  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.161  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.204  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.204  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.242  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.242  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.274  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.274  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.300  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.300  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.320  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.320  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.334  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.334  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.343  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.343  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.345  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.345  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.345  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:11:30.348  5509  5520 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 06:11:30.348  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.348  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.348  5509  5520 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:11:30.359  5509  5805 I .ghprotocol.app: Alloc concurrent copying GC freed 3600(162KB) AllocSpace objects, 4(80KB) LOS objects, 49% free, 6043KB/11MB, paused 14us,3us total 10.668ms
10-25 06:11:30.359  5509  5520 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 10.758ms
10-25 06:11:30.359  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:11:30.368  5509  5520 I .ghprotocol.app: Alloc concurrent copying GC freed 198(20KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6375KB/12MB, paused 41us,40us total 9.255ms
10-25 06:11:31.428  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36300) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:11:32.884  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42824) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:11:36.000  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42828) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:11:41.995  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42842) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:11:53.985  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38710) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:05.975  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34158) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:17.965  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 47762) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:29.954  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48016) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:31.385  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48020) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:31.386  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48034) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:31.595  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48036) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:32.028  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48038) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:32.891  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60580) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:34.588  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60592) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:38.075  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60606) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:41.944  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60616) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:44.987  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 44872) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:53.935  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60148) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:12:58.556  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60152) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:13:05.924  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52366) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:13:17.914  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59896) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:13:22.158  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:13:22.161  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.308  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.308  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.453  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.453  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.593  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.593  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.727  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.728  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.856  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.856  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.979  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:22.979  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.096  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.096  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.206  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.206  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.311  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.311  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.410  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.410  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.503  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.503  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.590  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.590  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.670  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.670  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.743  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.743  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.810  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.810  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.872  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.872  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.928  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.928  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.978  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:23.978  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.022  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.022  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.060  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.060  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.093  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.093  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.119  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.119  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.140  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.140  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.156  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.156  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.164  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.164  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.167  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.167  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.168  5509  5805 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:13:24.171  5509  5520 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 06:13:24.171  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.171  5509  5805 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.171  5509  5520 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:13:24.182  5509  5805 I .ghprotocol.app: Alloc concurrent copying GC freed 3894(176KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6041KB/11MB, paused 16us,4us total 10.693ms
10-25 06:13:24.182  5509  5520 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 10.851ms
10-25 06:13:24.182  5509  5520 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:13:24.192  5509  5520 I .ghprotocol.app: Alloc concurrent copying GC freed 335(46KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6379KB/12MB, paused 141us,9us total 10.220ms
10-25 06:13:25.435  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 57932) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:13:29.904  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 57948) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:13:41.893  5509  5805 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54026) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


