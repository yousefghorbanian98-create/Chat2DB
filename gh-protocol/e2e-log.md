## gh-protocol E2E log — 2026-10-25T07:15:50Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T07:07:35Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 07:04 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 07:07 .
drwxr-xr-x 3 runner runner 4096 Oct 25 07:07 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 07:07 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 07:07 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2853
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
WARNING: cannnot unmap ptr 0x7fc7a5801000 as it is in the protected range from 0x7fc6a5800000 to 0x7fc7a5a00000
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
INFO         | Boot completed in 29503 ms
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
> Task :app:generateDebugBuildConfig
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:parseDebugLocalResources
> Task :app:checkDebugAarMetadata
> Task :app:mergeDebugShaders
> Task :app:javaPreCompileDebug
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792911919179.json

BUILD SUCCESSFUL in 1m 56s
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
seeded cache: 37417 bytes, meta=1792912173994
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5651)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5651   336   14107440 180980 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:38815  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:36673  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:56406  ::ffff:142.251.150.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{b29b596 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a1cd1ac 5651:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~lHo9JTDhQrG3wyq4XxWzxA==/com.ghprotocol.app-9JknmoLUfxXWeTJega33dg==/base.apk
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
      windows=[Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m4s994ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{dddd4bd u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{a1cd1ac 5651:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~lHo9JTDhQrG3wyq4XxWzxA==/com.ghprotocol.app-9JknmoLUfxXWeTJega33dg==/base.apk
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
      windows=[Window{d520a6c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m12s854ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@47067230
  deepestLastOrientationSource=ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=99
  mCurrentFocus=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{dddd4bd u0 com.ghprotocol.app/.MainActivity t8}
      * Task{b02790c #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{faab92e #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{90defa9 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{c18c5f9 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{aaf139f #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{51ae84c u0 StatusBar}
    mFocusedWindow=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{c741d21 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
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
      Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {d9470000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=be82da1 InputMethod)/@0xf3902dd - animation-leash of insets_animation)/@0x9d924f5 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{be82da1 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=be82da1 InputMethod)/@0xf3902dd - animation-leash of insets_animation)/@0x9d924f5
        mControlTarget=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false
      InsetsSourceProvider
        mSource=InsetsSource id=d9470006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{51ae84c u0 StatusBar}
      InsetsSourceProvider
        mSource=InsetsSource id=d9470005 type=mandatorySystemGestures frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
--
        mWindowContainer=Window{51ae84c u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=51ae84c StatusBar)/@0x343d38 - animation-leash of insets_animation)/@0x535928a
        mControlTarget=Window{39dfc34 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false

--
        (multi-window) Task{a74593e #3 type=undefined}
        (multi-window) Task{aaf139f #4 type=undefined}
        (fullscreen) Task{5735ab2 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{a1cd1ac 5651:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 07:09 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 07:09 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 07:09 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 07:09 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 07:09 xray-err.log
-rw------- 1 u0_a192 u0_a192     506 2026-10-25 07:09 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 07:09:42.526291 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: app/proxyman/inbound: failed to listen TCP on 53 > transport/internet: failed to listen on address: 127.0.0.1:53 > transport/internet/tcp: failed to listen tcp on 127.0.0.1:53 > listen tcp 127.0.0.1:53: bind: permission denied
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 07:09:42.881  5651  5790 W GhDiag  : xray exited rc=255
GhDiag (connect-flow trace):
--------- beginning of main
10-25 07:09:42.080  5651  5651 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 07:09:42.080  5651  5651 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 07:09:42.311  5651  5651 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 07:09:42.327  5651  5651 D GhDiag  : connect: config written bytes=5427 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 07:09:42.500  5651  5651 D GhDiag  : connect: core.start=true 
10-25 07:09:42.881  5651  5790 W GhDiag  : xray exited rc=255
10-25 07:09:52.549  5651  5651 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 07:09:52.576  5651  5651 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@15135bf} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
lloc
10-25 07:10:53.173  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.241  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.241  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.306  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.306  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.367  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.368  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.426  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.426  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.480  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.480  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.531  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.531  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.578  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.578  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.622  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.622  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.662  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.662  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.699  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.699  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.733  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.733  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.763  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.763  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.791  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.791  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.814  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.814  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.834  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.834  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.850  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.850  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.863  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.863  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.873  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.873  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.879  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.879  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.882  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.882  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.882  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:10:53.884  5651  5662 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:10:53.884  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.884  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.884  5651  5662 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:10:53.893  5651  5895 I .ghprotocol.app: Alloc concurrent copying GC freed 5635(231KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 6437KB/12MB, paused 10us,3us total 9.043ms
10-25 07:10:53.894  5651  5662 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 9.350ms
10-25 07:10:53.894  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:10:53.902  5651  5662 I .ghprotocol.app: Alloc concurrent copying GC freed 5007(204KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6808KB/13MB, paused 212us,6us total 8.388ms
10-25 07:12:02.399  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:12:02.402  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.491  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.491  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.579  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.579  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.663  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.664  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.744  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.744  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.821  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.821  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.902  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.902  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.973  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:02.973  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.041  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.041  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.106  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.106  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.165  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.166  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.222  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.222  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.274  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.274  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.325  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.325  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.372  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.372  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.417  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.417  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.457  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.457  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.495  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.495  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.530  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.530  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.561  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.561  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.589  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.589  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.615  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.615  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.637  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.637  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.655  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.655  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.671  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.671  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.682  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.682  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.691  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.691  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.696  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.696  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.698  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.698  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.698  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:12:03.699  5651  5662 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:12:03.699  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.700  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.700  5651  5662 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:12:03.707  5651  5895 I .ghprotocol.app: Alloc concurrent copying GC freed 3761(176KB) AllocSpace objects, 4(80KB) LOS objects, 49% free, 6184KB/12MB, paused 8us,3us total 7.857ms
10-25 07:12:03.707  5651  5662 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 7.904ms
10-25 07:12:03.707  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:12:03.715  5651  5662 I .ghprotocol.app: Alloc concurrent copying GC freed 187(20KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6660KB/13MB, paused 34us,5us total 7.086ms
10-25 07:13:08.725  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:13:08.727  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.812  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.812  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.896  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.896  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.976  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:08.976  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.053  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.053  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.127  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.127  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.196  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.196  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.263  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.263  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.327  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.327  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.388  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.388  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.443  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.443  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.497  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.497  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.547  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.547  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.593  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.593  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.637  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.637  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.678  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.678  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.716  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.716  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.750  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.750  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.782  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.782  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.809  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.809  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.834  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.834  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.855  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.855  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.873  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.873  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.887  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.887  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.899  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.899  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.907  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.907  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.912  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.912  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.914  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.914  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.914  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:13:09.916  5651  5662 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:13:09.916  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.916  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.916  5651  5662 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:13:09.923  5651  5895 I .ghprotocol.app: Alloc concurrent copying GC freed 3692(172KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6180KB/12MB, paused 8us,3us total 7.437ms
10-25 07:13:09.923  5651  5662 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 7.477ms
10-25 07:13:09.923  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:13:09.930  5651  5662 I .ghprotocol.app: Alloc concurrent copying GC freed 95(16KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6660KB/13MB, paused 33us,5us total 7.095ms
10-25 07:13:42.136  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42090) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:13:43.594  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42100) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:13:46.591  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42108) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:13:52.586  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39542) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:04.574  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38440) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:16.042  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:14:16.045  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.131  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.131  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.215  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.215  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.296  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.296  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.374  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.374  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.449  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.449  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.521  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.521  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.564  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55858) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:16.591  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.591  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.657  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.657  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.719  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.719  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.777  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.777  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.832  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.832  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.883  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.884  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.932  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.932  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.977  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:16.977  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.019  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.019  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.058  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.058  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.093  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.093  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.126  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.126  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.155  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.155  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.180  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.180  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.202  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.202  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.220  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.220  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.235  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.235  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.247  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.247  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.255  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.255  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.260  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.260  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.262  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.262  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.262  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:14:17.264  5651  5662 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:14:17.264  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:17.264  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:14:17.271  5651  5662 I .ghprotocol.app: Alloc concurrent copying GC freed 3736(170KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6180KB/12MB, paused 6us,3us total 7.737ms
10-25 07:14:17.271  5651  5895 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 9.477ms
10-25 07:14:17.271  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:14:28.552  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56282) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:40.544  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42184) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:42.103  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42192) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:42.104  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42206) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:42.315  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42216) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:42.760  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42228) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:43.623  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42230) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:45.351  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42236) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:49.000  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41290) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:52.530  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41292) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:14:55.911  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41296) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:04.519  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34202) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:09.735  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46836) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:14.707  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:15:14.710  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.785  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.785  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.859  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.859  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.929  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.929  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.995  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:14.995  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.059  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.059  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.118  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.118  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.175  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.175  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.228  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.228  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.277  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.277  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.323  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.323  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.366  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.366  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.405  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.405  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.442  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.442  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.474  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.474  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.503  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.503  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.529  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.529  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.551  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.551  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.570  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.570  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.586  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.586  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.602  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.602  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.611  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.611  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.618  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.618  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.620  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.620  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.620  5651  5895 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:15:15.622  5651  5662 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:15:15.622  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.622  5651  5895 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.622  5651  5662 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:15:15.630  5651  5895 I .ghprotocol.app: Alloc concurrent copying GC freed 3835(175KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6182KB/12MB, paused 9us,3us total 8.065ms
10-25 07:15:15.630  5651  5662 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 8.102ms
10-25 07:15:15.630  5651  5662 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:15:15.637  5651  5662 I .ghprotocol.app: Alloc concurrent copying GC freed 432(39KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6622KB/12MB, paused 33us,5us total 7.017ms
10-25 07:15:16.510  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46848) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:28.499  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48930) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:37.640  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37844) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:15:40.670  5651  5895 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37854) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


