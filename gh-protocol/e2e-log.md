## gh-protocol E2E log — 2026-10-25T06:25:35Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T06:16:54Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 06:11 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 06:17 .
drwxr-xr-x 3 runner runner 4096 Oct 25 06:17 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 06:17 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 06:17 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3066
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
WARNING: cannnot unmap ptr 0x7f7e21c01000 as it is in the protected range from 0x7f7d21c00000 to 0x7f7e21e00000
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
INFO         | Boot completed in 39330 ms
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
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
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
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:parseDebugLocalResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug
> Task :app:processDebugResources
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792908858042.json

BUILD SUCCESSFUL in 2m 31s
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
seeded cache: 37417 bytes, meta=1792909148742
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5253)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5253   336   13768492 176476 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:39793  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:33843  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:50638  ::ffff:142.251.155.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{5471a33 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{308b218 5253:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~pVI1Cg3lRKAVT3VyKMSagQ==/com.ghprotocol.app-s7Z1PfcB7mPaJTJ78dXVMw==/base.apk
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
      windows=[Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m15s390ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{77cf3a6 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{308b218 5253:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~pVI1Cg3lRKAVT3VyKMSagQ==/com.ghprotocol.app-s7Z1PfcB7mPaJTJ78dXVMw==/base.apk
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
      windows=[Window{1c4cdad u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m21s973ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@58335622
  deepestLastOrientationSource=ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=95
  mCurrentFocus=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{77cf3a6 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{bea7274 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{509e35a #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{729104e u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{292bd9 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{a719c7f #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{488360c u0 StatusBar}
    mFocusedWindow=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=60ae0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {60ae0000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=60ae0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{488360c u0 StatusBar}
--
        mWindowContainer=Window{488360c u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=488360c StatusBar)/@0x288a6f8 - animation-leash of insets_animation)/@0x818b67
        mControlTarget=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=d0d584c InputMethod)/@0xb67659b - animation-leash of insets_animation)/@0x84bed14 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{d0d584c u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=d0d584c InputMethod)/@0xb67659b - animation-leash of insets_animation)/@0x84bed14
        mControlTarget=Window{ae97fc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{fb9f99e #3 type=undefined}
        (multi-window) Task{a719c7f #4 type=undefined}
        (fullscreen) Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{308b218 5253:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6216
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 06:19 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 06:19 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 06:19 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 06:19 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 06:19 xray-err.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-25 06:19:16.945  5253  5253 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:19:16.946  5253  5253 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:19:17.127  5253  5253 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:19:17.149  5253  5253 D GhDiag  : connect: config written bytes=5564 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:19:17.277  5253  5253 D GhDiag  : connect: core.start=true 
10-25 06:19:28.390  5253  5253 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:19:28.526  5253  5253 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@fdcc57e} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
0, 2400) d=0}]}
10-25 06:19:17.592   523   541 V WindowManager: Sent Transition #7 createdAt=10-25 06:19:16.775 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=114214 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{d3a6ad5 Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{28fea94 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:19:17.592   833   864 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity)/@0xa141190 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{77cf3a6 u0 com.ghprotocol.app/.MainActivity)/@0xd458a89 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:19:17.592   523   541 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d1deec9 u0 com.ghprotocol.app/.MainActivity)/@0x22794a6 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{77cf3a6 u0 com.ghprotocol.app/.MainActivity)/@0xb7fae01 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:19:17.831   833   864 V WindowManagerShell: Transition requested: android.os.BinderProxy@b3549f2 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=115119 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@5646843} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{a56fec0 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:19:18.074   523  2124 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 06:19:18.078   523  2124 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 06:19:18.078   523  2124 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 06:19:18.890   523   541 V WindowManager: Sent Transition #8 createdAt=10-25 06:19:17.630 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=115119 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{d3a6ad5 Task{ad481e7 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{225ed9d com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:19:19.397  5253  5270 I .ghprotocol.app: Background concurrent copying GC freed 112054(5664KB) AllocSpace objects, 30(896KB) LOS objects, 49% free, 6486KB/12MB, paused 22us,6us total 104.764ms
10-25 06:19:19.618   523   576 I AppsFilter: interaction: PackageSetting{7d5e0f9 com.ghprotocol.app/10192} -> PackageSetting{a32d83e com.google.android.contacts/10155} BLOCKED
10-25 06:19:22.866   523   576 I AppsFilter: interaction: PackageSetting{7d5e0f9 com.ghprotocol.app/10192} -> PackageSetting{cf59008 com.google.android.googlequicksearchbox/10131} BLOCKED
10-25 06:19:25.630  5636  5636 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 06:19:25.638  5636  5636 I AndroidRuntime: Using default boot image
10-25 06:19:25.639  5636  5636 I AndroidRuntime: Leaving lock profiling enabled
10-25 06:19:25.989  5636  5636 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 06:19:27.078  5636  5636 D AndroidRuntime: Shutting down VM
10-25 06:19:28.335   523  2549 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 06:19:28.390  5253  5253 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:19:28.526   523   902 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 06:19:28.526  5253  5253 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@fdcc57e} — relay loop started
10-25 06:19:28.729   523   902 I ImeTracker: com.ghprotocol.app:f8e64d1b: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 06:19:28.729   523   902 I ImeTracker: com.ghprotocol.app:f8e64d1b: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:19:28.732  1545  1545 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:19:28.865  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55726) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:29.058  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55742) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:29.478  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55754) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:30.307  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55768) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:31.974  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55774) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:34.185   523   576 I AppsFilter: interaction: PackageSetting{7d5e0f9 com.ghprotocol.app/10192} -> PackageSetting{80bf53b com.google.android.contacts/10155} BLOCKED
10-25 06:19:35.431  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34350) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:40.163  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34356) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:41.186  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34364) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:42.083  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34370) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:43.202  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34384) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:47.458  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 53418) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:55.394  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55336) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:19:55.650  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55344) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:20:13.716   523   576 I AppsFilter: interaction: PackageSetting{7d5e0f9 com.ghprotocol.app/10192} -> PackageSetting{ce84e10 com.google.android.contacts/10155} BLOCKED
10-25 06:20:21.762  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39438) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:20:23.724   523   576 I AppsFilter: interaction: PackageSetting{7d5e0f9 com.ghprotocol.app/10192} -> PackageSetting{1d0790f com.google.android.contacts/10155} BLOCKED
10-25 06:21:15.641  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:21:15.645  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:15.838  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:15.839  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:15.846  5253  5667 I .ghprotocol.app: Alloc young concurrent copying GC freed 66976(5903KB) AllocSpace objects, 0(0B) LOS objects, 46% free, 6901KB/12MB, paused 30us,5us total 6.458ms
10-25 06:21:15.997  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:15.997  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.124  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.124  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.246  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.246  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.360  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.360  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.469  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.469  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.572  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.572  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.669  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.669  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.761  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.761  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.850  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.850  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.928  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:16.928  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.001  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.001  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.068  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.068  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.130  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.130  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.187  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.187  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.238  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.238  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.283  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.283  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.323  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.323  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.356  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.356  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.383  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.383  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.404  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.404  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.419  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.419  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.428  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.428  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.431  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.431  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:21:17.438  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:21:17.444  5253  5272 I .ghprotocol.app: Alloc concurrent copying GC freed 8437(478KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 6447KB/12MB, paused 19us,4us total 12.208ms
10-25 06:21:17.444  5253  5667 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.591ms
10-25 06:21:17.444  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:04.813  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:23:04.817  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:04.954  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:04.954  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.088  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.088  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.216  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.216  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.338  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.338  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.453  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.453  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.563  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.563  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.667  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.667  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.766  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.766  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.858  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.858  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.944  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:05.944  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.025  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.025  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.100  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.100  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.168  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.168  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.231  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.231  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.288  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.288  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.339  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.339  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.384  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.384  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.424  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.424  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.457  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.457  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.483  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.483  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.504  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.504  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.520  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.520  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.529  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.529  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.531  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.531  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:06.538  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:23:06.544  5253  5272 I .ghprotocol.app: Alloc concurrent copying GC freed 6377(416KB) AllocSpace objects, 4(80KB) LOS objects, 49% free, 6365KB/12MB, paused 19us,3us total 12.034ms
10-25 06:23:06.544  5253  5667 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.245ms
10-25 06:23:06.544  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:23:16.998  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56538) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:23:18.456  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56550) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:23:21.454  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56560) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:23:27.819  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56428) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:23:39.809  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46444) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:23:51.799  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41704) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:03.790  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40908) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:15.993  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42032) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:16.957  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42044) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:16.958  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42060) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:17.166  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42074) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:17.602  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42086) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:18.466  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42094) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:20.162  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42100) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:23.682  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49926) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:27.983  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49930) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:30.594  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49946) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:39.973  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 47772) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:44.162  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45288) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:51.962  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45304) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:24:52.402  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:24:52.406  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.541  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.541  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.674  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.674  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.802  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.802  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.923  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:52.923  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.038  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.038  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.148  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.148  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.253  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.253  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.352  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.352  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.445  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.445  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.532  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.532  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.613  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.613  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.688  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.689  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.758  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.758  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.821  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.821  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.877  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.877  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.928  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.928  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.973  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:53.973  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.012  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.012  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.045  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.045  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.072  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.073  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.094  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.094  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.110  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.110  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.119  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.119  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.122  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.122  5253  5272 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:24:54.129  5253  5667 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:24:54.134  5253  5272 I .ghprotocol.app: Alloc concurrent copying GC freed 6822(442KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6347KB/12MB, paused 19us,3us total 12.310ms
10-25 06:24:54.135  5253  5667 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.591ms
10-25 06:24:54.135  5253  5667 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:25:03.952  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52748) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:25:12.578  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52754) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:25:15.941  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50778) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:25:27.930  5253  5667 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 57302) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


