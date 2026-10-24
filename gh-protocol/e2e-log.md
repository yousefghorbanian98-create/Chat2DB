## gh-protocol E2E log — 2026-10-24T21:56:05Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-24T21:46:54Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 24 21:43 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 1.7G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 24 21:47 .
drwxr-xr-x 3 runner runner 4096 Oct 24 21:47 ..
drwxr-xr-x 3 runner runner 4096 Oct 24 21:47 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 24 21:47 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/default/x86_64/
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
ERROR        | Unable to connect to adb daemon on port: 5037
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3056
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
INFO         |   androidboot.vbmeta.digest=8bee4f6105b6acd7de887b1ee6629ab07066df02ee9bbca07663adffdad97fc1
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7f8840201000 as it is in the protected range from 0x7f8740200000 to 0x7f8840400000
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
INFO         | Boot completed in 29824 ms
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
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
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
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs
> Task :app:compressDebugAssets
> Task :app:mergeLibDexDebug
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeExtDexDebug
> Task :app:processDebugResources
> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792878262985.json

BUILD SUCCESSFUL in 2m 35s
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
seeded cache: 37417 bytes, meta=1792878530302
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2369)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a141       2369   327   13932020 174424 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:50204  ::ffff:172.217.115.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{3e1258c 2369:com.ghprotocol.app/u0a141}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.34 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-7m5s142ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=false
    * Hist  #0: ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{3e1258c 2369:com.ghprotocol.app/u0a141}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.34 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.1 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{216f04a u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-7m12s238ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=true mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@172815283
  deepestLastOrientationSource=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.34 fontWeightAdjustment=0}
  mLayoutSeq=68
  mCurrentFocus=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  Display areas in top down Z order:
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}
      mLastFocusedRootTask=Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{54bb8e9 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{aea05b8 #7 type=home I=com.android.launcher3/.uioverrides.QuickstepLauncher U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{3d01b u0 com.android.launcher3/.uioverrides.QuickstepLauncher t7}
      * Task{a4e897c #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{53f125a #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{b0ece1c u0 StatusBar}
    mFocusedWindow=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
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
      Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(540, 2400) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {b8380000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(540, 2400 - 540, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=78e0bd5 InputMethod)/@0x70712db - animation-leash of insets_animation)/@0x6c3dd6a mInitiallyVisible=false mSurfacePosition=Point(540, 2400) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{78e0bd5 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=78e0bd5 InputMethod)/@0x70712db - animation-leash of insets_animation)/@0x6c3dd6a
        mControlTarget=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false
      InsetsSourceProvider
        mSource=InsetsSource id=b8380006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{b0ece1c u0 StatusBar}
      InsetsSourceProvider
        mSource=InsetsSource id=b8380005 type=mandatorySystemGestures frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
--
        mWindowContainer=Window{b0ece1c u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=b0ece1c StatusBar)/@0x12ff64c - animation-leash of insets_animation)/@0x8d7c25b
        mControlTarget=Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false

--
        (multi-window) Task{33c8205 #3 type=undefined}
        (multi-window) Task{53f125a #4 type=undefined}
        (fullscreen) Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{3e1258c 2369:com.ghprotocol.app/u0a141}]
  NumNonAppVisibleWindowUidMap:[ 10117:1]
app filesDir/xray:
total 79624
drwx------ 2 u0_a141 u0_a141     4096 2026-10-24 21:48 .
drwxrwxrwx 3 u0_a141 u0_a141     4096 2026-10-24 21:48 ..
-rwx--x--x 1 u0_a141 u0_a141 38872056 2026-10-24 21:48 Xray
-rw------- 1 u0_a141 u0_a141 36282168 2026-10-24 21:48 Xray-arm64-v8a
-rw------- 1 u0_a141 u0_a141  3977011 2026-10-24 21:48 geoip.dat
-rw------- 1 u0_a141 u0_a141  2358471 2026-10-24 21:48 geosite.dat
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-24 21:48:58.438  2369  2369 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-24 21:48:58.439  2369  2369 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-24 21:48:58.850  2369  2369 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-24 21:48:58.850  2369  2369 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
ol.app.MainActivity}
10-24 21:47:50.665   999   999 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-24 21:47:50.708   999   999 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-24 21:47:50.713   999  1288 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-24 21:47:50.721   999  1288 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-24 21:47:51.907   506   559 I AppsFilter: interaction: PackageSetting{ae93d8a com.ghprotocol.app/10141} -> PackageSetting{8cb6ffb com.android.camera2/10104} BLOCKED
10-24 21:47:51.907   506   559 I AppsFilter: interaction: PackageSetting{ae93d8a com.ghprotocol.app/10141} -> PackageSetting{3800271 com.android.calendar/10099} BLOCKED
10-24 21:47:51.907   506   559 I AppsFilter: interaction: PackageSetting{ae93d8a com.ghprotocol.app/10141} -> PackageSetting{2a5a856 com.android.rkpdapp/10124} BLOCKED
10-24 21:47:51.907   506   559 I AppsFilter: interaction: PackageSetting{ae93d8a com.ghprotocol.app/10141} -> PackageSetting{25710d7 com.android.inputmethod.latin/10109} BLOCKED
10-24 21:47:51.907   506   559 I AppsFilter: interaction: PackageSetting{ae93d8a com.ghprotocol.app/10141} -> PackageSetting{37dddc4 com.android.cellbroadcastreceiver.module/10130} BLOCKED
10-24 21:48:50.200   506  2228 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-24 21:48:50.202   506  2228 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 21:48:50.202   798   831 V WindowManagerShell: Transition requested: android.os.BinderProxy@f842d6f TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=91691 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@3f95a7c} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2a57f05 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:48:50.214   506   536 I ActivityManager: Start proc 2369:com.ghprotocol.app/u0a141 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-24 21:48:50.240   506  1679 D CoreBackPreview: Window{ab49a24 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@f70f742, mPriority=0, mIsAnimationCallback=false}
10-24 21:48:50.365  2369  2369 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-24 21:48:50.377  2369  2369 I .ghprotocol.app: Using CollectorTypeCC GC.
10-24 21:48:50.378  2369  2369 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-24 21:48:50.378  2369  2369 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-24 21:48:50.582   506   523 V WindowManager: Sent Transition #6 createdAt=10-24 21:48:50.197 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=91691 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{85105a8 Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{228c8c1 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:48:50.582   506   523 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{85105a8 Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x9b33490 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{ece7866 Task{54bb8e9 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xfad2f53 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:48:50.620  2369  2369 W ziparchive: Unable to open '/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.dm': No such file or directory
10-24 21:48:50.622  2369  2369 W ziparchive: Unable to open '/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.dm': No such file or directory
10-24 21:48:50.877  2369  2369 D nativeloader: Configuring clns-6 for other apk /data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/lib/x86_64:/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-24 21:48:50.883  2369  2369 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-24 21:48:50.883  2369  2369 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: and incorrect proguard optimizations.
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:48:51.209  2369  2369 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 21:48:51.255   506  2228 D CoreBackPreview: Window{216f04a u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@dd3733, mPriority=0, mIsAnimationCallback=false}
10-24 21:48:51.885   506   523 W ziparchive: Unable to open '/data/app/~~prnrT9ienvS_Wyj3cIThIA==/com.ghprotocol.app-qcwCTg1qpi7dHue4NlzGWg==/base.dm': No such file or directory
10-24 21:48:51.886   506   523 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s691ms
10-24 21:48:51.901   506  1326 D CoreBackPreview: Window{ab49a24 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-24 21:48:51.901   506  1326 W InputManager-JNI: Input channel object 'ab49a24 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 21:48:51.906   506  1326 I ImeTracker: com.ghprotocol.app:83a9fb72: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-24 21:48:51.907   506  1326 I ImeTracker: com.ghprotocol.app:83a9fb72: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-24 21:48:56.240  2369  2416 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-24 21:48:58.262   506  2228 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 21:48:58.262   798   831 V WindowManagerShell: Transition requested: android.os.BinderProxy@c584c86 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=99750 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@e8d9947} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{ae81574 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:48:58.438  2369  2369 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-24 21:48:58.439  2369  2369 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-24 21:48:58.838  2430  2430 W .ghprotocol.app: type=1400 audit(0.0:15): avc:  granted  { execute } for  name="Xray" dev="dm-38" ino=131274 scontext=u:r:untrusted_app:s0:c141,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c141,c256,c512,c768 tclass=file app=com.ghprotocol.app
10-24 21:48:58.838  2430  2430 W .ghprotocol.app: type=1400 audit(0.0:16): avc:  denied  { execute_no_trans } for  path="/data/data/com.ghprotocol.app/files/xray/Xray" dev="dm-38" ino=131274 scontext=u:r:untrusted_app:s0:c141,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c141,c256,c512,c768 tclass=file permissive=0 app=com.ghprotocol.app
10-24 21:48:58.850  2369  2369 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-24 21:48:58.850  2369  2369 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
10-24 21:48:58.877   506   520 D CoreBackPreview: Window{bd8304e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@9f2d27c, mPriority=0, mIsAnimationCallback=false}
10-24 21:48:58.997   798   831 V WindowManagerShell: onTransitionReady android.os.BinderProxy@c584c86: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity)/@0x712aa9d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity)/@0x55cab12 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:48:58.997   798   831 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity)/@0x712aa9d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity)/@0x55cab12 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:48:58.997   798   831 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity)/@0x712aa9d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity)/@0x55cab12 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:48:59.001   506   523 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +737ms
10-24 21:48:59.001   506   523 V WindowManager: Sent Transition #7 createdAt=10-24 21:48:58.258 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=99750 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{85105a8 Task{ff5893a #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b65fb26 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:48:59.001   506   523 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{81e4b13 u0 com.ghprotocol.app/.MainActivity)/@0xcd89a68 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4390865 u0 com.ghprotocol.app/.MainActivity)/@0x8d2098b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:48:59.219   506  1326 I ImeTracker: com.ghprotocol.app:f6bc319a: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-24 21:48:59.219   506  1326 I ImeTracker: com.ghprotocol.app:f6bc319a: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-24 21:49:06.593  2451  2451 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:49:06.596  2451  2451 I AndroidRuntime: Using default boot image
10-24 21:49:06.596  2451  2451 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:49:06.676  2451  2451 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:49:07.782  2451  2451 D AndroidRuntime: Shutting down VM
10-24 21:49:20.881  2478  2478 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:49:20.884  2478  2478 I AndroidRuntime: Using default boot image
10-24 21:49:20.884  2478  2478 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:49:20.957  2478  2478 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:49:22.012  2478  2478 D AndroidRuntime: Shutting down VM
10-24 21:49:35.097  2501  2501 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:49:35.100  2501  2501 I AndroidRuntime: Using default boot image
10-24 21:49:35.100  2501  2501 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:49:35.174  2501  2501 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:49:36.223  2501  2501 D AndroidRuntime: Shutting down VM
10-24 21:49:49.316  2526  2526 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:49:49.319  2526  2526 I AndroidRuntime: Using default boot image
10-24 21:49:49.319  2526  2526 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:49:49.396  2526  2526 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:49:50.446  2526  2526 D AndroidRuntime: Shutting down VM
10-24 21:50:03.486  2551  2551 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:50:03.489  2551  2551 I AndroidRuntime: Using default boot image
10-24 21:50:03.489  2551  2551 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:50:03.562  2551  2551 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:50:04.616  2551  2551 D AndroidRuntime: Shutting down VM
10-24 21:50:17.662  2575  2575 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:50:17.665  2575  2575 I AndroidRuntime: Using default boot image
10-24 21:50:17.665  2575  2575 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:50:17.741  2575  2575 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:50:18.791  2575  2575 D AndroidRuntime: Shutting down VM
10-24 21:50:31.855  2601  2601 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:50:31.859  2601  2601 I AndroidRuntime: Using default boot image
10-24 21:50:31.859  2601  2601 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:50:31.935  2601  2601 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:50:32.989  2601  2601 D AndroidRuntime: Shutting down VM
10-24 21:50:46.023  2624  2624 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:50:46.026  2624  2624 I AndroidRuntime: Using default boot image
10-24 21:50:46.026  2624  2624 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:50:46.102  2624  2624 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:50:47.163  2624  2624 D AndroidRuntime: Shutting down VM
10-24 21:51:00.219  2649  2649 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:51:00.222  2649  2649 I AndroidRuntime: Using default boot image
10-24 21:51:00.222  2649  2649 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:51:00.297  2649  2649 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:51:01.347  2649  2649 D AndroidRuntime: Shutting down VM
10-24 21:51:14.397  2674  2674 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:51:14.400  2674  2674 I AndroidRuntime: Using default boot image
10-24 21:51:14.400  2674  2674 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:51:14.475  2674  2674 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:51:15.533  2674  2674 D AndroidRuntime: Shutting down VM
10-24 21:51:28.573  2698  2698 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:51:28.577  2698  2698 I AndroidRuntime: Using default boot image
10-24 21:51:28.577  2698  2698 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:51:28.651  2698  2698 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:51:29.707  2698  2698 D AndroidRuntime: Shutting down VM
10-24 21:51:42.850  2723  2723 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:51:42.853  2723  2723 I AndroidRuntime: Using default boot image
10-24 21:51:42.853  2723  2723 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:51:42.932  2723  2723 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:51:43.983  2723  2723 D AndroidRuntime: Shutting down VM
10-24 21:51:57.043  2746  2746 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:51:57.046  2746  2746 I AndroidRuntime: Using default boot image
10-24 21:51:57.046  2746  2746 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:51:57.121  2746  2746 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:51:58.176  2746  2746 D AndroidRuntime: Shutting down VM
10-24 21:52:11.235  2771  2771 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:52:11.238  2771  2771 I AndroidRuntime: Using default boot image
10-24 21:52:11.238  2771  2771 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:52:11.315  2771  2771 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:52:12.365  2771  2771 D AndroidRuntime: Shutting down VM
10-24 21:52:25.472  2798  2798 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:52:25.476  2798  2798 I AndroidRuntime: Using default boot image
10-24 21:52:25.476  2798  2798 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:52:25.550  2798  2798 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:52:26.591  2798  2798 D AndroidRuntime: Shutting down VM
10-24 21:52:39.682  2822  2822 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:52:39.686  2822  2822 I AndroidRuntime: Using default boot image
10-24 21:52:39.686  2822  2822 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:52:39.763  2822  2822 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:52:40.812  2822  2822 D AndroidRuntime: Shutting down VM
10-24 21:52:53.877  2848  2848 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:52:53.880  2848  2848 I AndroidRuntime: Using default boot image
10-24 21:52:53.880  2848  2848 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:52:53.954  2848  2848 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:52:55.000  2848  2848 D AndroidRuntime: Shutting down VM
10-24 21:53:08.046  2871  2871 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:53:08.049  2871  2871 I AndroidRuntime: Using default boot image
10-24 21:53:08.049  2871  2871 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:53:08.130  2871  2871 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:53:09.174  2871  2871 D AndroidRuntime: Shutting down VM
10-24 21:53:22.244  2896  2896 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:53:22.247  2896  2896 I AndroidRuntime: Using default boot image
10-24 21:53:22.247  2896  2896 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:53:22.323  2896  2896 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:53:23.374  2896  2896 D AndroidRuntime: Shutting down VM
10-24 21:53:36.430  2922  2922 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:53:36.433  2922  2922 I AndroidRuntime: Using default boot image
10-24 21:53:36.433  2922  2922 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:53:36.506  2922  2922 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:53:37.551  2922  2922 D AndroidRuntime: Shutting down VM
10-24 21:53:50.584  2945  2945 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:53:50.587  2945  2945 I AndroidRuntime: Using default boot image
10-24 21:53:50.587  2945  2945 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:53:50.661  2945  2945 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:53:51.703  2945  2945 D AndroidRuntime: Shutting down VM
10-24 21:54:04.749  2970  2970 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:54:04.752  2970  2970 I AndroidRuntime: Using default boot image
10-24 21:54:04.752  2970  2970 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:54:04.826  2970  2970 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:54:05.874  2970  2970 D AndroidRuntime: Shutting down VM
10-24 21:54:18.923  2993  2993 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:54:18.926  2993  2993 I AndroidRuntime: Using default boot image
10-24 21:54:18.926  2993  2993 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:54:19.003  2993  2993 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:54:20.050  2993  2993 D AndroidRuntime: Shutting down VM
10-24 21:54:33.114  3018  3018 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:54:33.117  3018  3018 I AndroidRuntime: Using default boot image
10-24 21:54:33.117  3018  3018 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:54:33.194  3018  3018 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:54:34.246  3018  3018 D AndroidRuntime: Shutting down VM
10-24 21:54:47.258  3043  3043 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:54:47.261  3043  3043 I AndroidRuntime: Using default boot image
10-24 21:54:47.261  3043  3043 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:54:47.334  3043  3043 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:54:48.389  3043  3043 D AndroidRuntime: Shutting down VM
10-24 21:55:01.435  3066  3066 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:55:01.438  3066  3066 I AndroidRuntime: Using default boot image
10-24 21:55:01.438  3066  3066 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:55:01.515  3066  3066 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:55:02.556  3066  3066 D AndroidRuntime: Shutting down VM
10-24 21:55:15.600  3091  3091 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:55:15.603  3091  3091 I AndroidRuntime: Using default boot image
10-24 21:55:15.603  3091  3091 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:55:15.678  3091  3091 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:55:16.725  3091  3091 D AndroidRuntime: Shutting down VM
10-24 21:55:29.752  3114  3114 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:55:29.755  3114  3114 I AndroidRuntime: Using default boot image
10-24 21:55:29.755  3114  3114 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:55:29.831  3114  3114 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:55:30.882  3114  3114 D AndroidRuntime: Shutting down VM
10-24 21:55:43.935  3139  3139 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:55:43.938  3139  3139 I AndroidRuntime: Using default boot image
10-24 21:55:43.938  3139  3139 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:55:44.016  3139  3139 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:55:45.059  3139  3139 D AndroidRuntime: Shutting down VM
10-24 21:55:58.090  3164  3164 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:55:58.094  3164  3164 I AndroidRuntime: Using default boot image
10-24 21:55:58.094  3164  3164 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:55:58.172  3164  3164 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:55:59.213  3164  3164 D AndroidRuntime: Shutting down VM


