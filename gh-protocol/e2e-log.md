## gh-protocol E2E log — 2026-10-25T07:42:22Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T07:34:04Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 07:30 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 07:34 .
drwxr-xr-x 3 runner runner 4096 Oct 25 07:34 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 07:34 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 07:34 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2820
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
WARNING: cannnot unmap ptr 0x7f8c0c401000 as it is in the protected range from 0x7f8b0c400000 to 0x7f8c0c600000
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
INFO         | Boot completed in 31834 ms
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
> Task :app:packageDebugResources
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:checkDebugDuplicateClasses
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792913505658.json

BUILD SUCCESSFUL in 2m 2s
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
seeded cache: 37417 bytes, meta=1792913765726
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5614)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5614   336   14129088 181580 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:35013  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:41435  [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:57640  ::ffff:142.251.157.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{4bbdd02 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{1cd21b6 5614:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~B4X-nqNRSLcS6YOv2i_93A==/com.ghprotocol.app-7MTGZXeGIPHco6ocRaZxSA==/base.apk
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
      windows=[Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m6s3ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{7b9e0ea u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{1cd21b6 5614:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~B4X-nqNRSLcS6YOv2i_93A==/com.ghprotocol.app-7MTGZXeGIPHco6ocRaZxSA==/base.apk
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
      windows=[Window{2c48909 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m13s7ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@201297657
  deepestLastOrientationSource=ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=96
  mCurrentFocus=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{7b9e0ea u0 com.ghprotocol.app/.MainActivity t8}
      * Task{741849f #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{80a9d51 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{49a1278 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{2b50c #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{f79906a #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{ab1372e u0 StatusBar}
    mFocusedWindow=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{eeed708 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=3a540006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3a540000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=3a540006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{ab1372e u0 StatusBar}
--
        mWindowContainer=Window{ab1372e u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=ab1372e StatusBar)/@0x59d983a - animation-leash of insets_animation)/@0x140cdb9
        mControlTarget=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=b507e29 InputMethod)/@0xbb67f4f - animation-leash of insets_animation)/@0xd5c25fe mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{b507e29 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=b507e29 InputMethod)/@0xbb67f4f - animation-leash of insets_animation)/@0xd5c25fe
        mControlTarget=Window{ab41087 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{798ee55 #3 type=undefined}
        (multi-window) Task{f79906a #4 type=undefined}
        (fullscreen) Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{1cd21b6 5614:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 07:36 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 07:36 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 07:36 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 07:36 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 07:36 xray-err.log
-rw------- 1 u0_a192 u0_a192     335 2026-10-25 07:36 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 07:36:13.936627 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: listen udp 127.0.0.1:5353: bind: address already in use
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 07:36:14.527  5614  5735 W GhDiag  : xray exited rc=255
GhDiag (connect-flow trace):
--------- beginning of main
10-25 07:36:13.791  5614  5614 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 07:36:13.792  5614  5614 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 07:36:13.882  5614  5614 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 07:36:13.897  5614  5614 D GhDiag  : connect: config written bytes=5429 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 07:36:13.920  5614  5614 D GhDiag  : connect: core.start=true 
10-25 07:36:14.527  5614  5735 W GhDiag  : xray exited rc=255
10-25 07:36:24.101  5614  5614 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 07:36:24.137  5614  5614 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@e96536} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
izeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@2375e9a} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{58263cb com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 07:36:14.364   520   533 I ImeTracker: com.ghprotocol.app:80b13710: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 07:36:14.364   520   533 I ImeTracker: com.ghprotocol.app:80b13710: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 07:36:14.381  1499  1499 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 07:36:14.445   520  2465 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 07:36:14.446   520  2465 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 07:36:14.446   520  2465 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 07:36:14.527  5614  5735 W GhDiag  : xray exited rc=255
10-25 07:36:14.878   520   537 V WindowManager: Sent Transition #8 createdAt=10-25 07:36:14.161 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=103732 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{690c09f Task{ba83fdb #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5df4d3f com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 07:36:15.081   520   571 I AppsFilter: interaction: PackageSetting{263096a com.ghprotocol.app/10192} -> PackageSetting{3057e5b com.google.android.contacts/10155} BLOCKED
10-25 07:36:16.211   520   571 I AppsFilter: interaction: PackageSetting{263096a com.ghprotocol.app/10192} -> PackageSetting{e940c1 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 07:36:21.968  5828  5828 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 07:36:21.972  5828  5828 I AndroidRuntime: Using default boot image
10-25 07:36:21.972  5828  5828 I AndroidRuntime: Leaving lock profiling enabled
10-25 07:36:22.045  5828  5828 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 07:36:23.081  5828  5828 D AndroidRuntime: Shutting down VM
10-25 07:36:24.070   520  1625 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 07:36:24.101  5614  5614 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 07:36:24.137   520  1456 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 07:36:24.137  5614  5614 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@e96536} — relay loop started
10-25 07:36:24.359   520  1456 I ImeTracker: com.ghprotocol.app:20cfa38c: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 07:36:24.359   520  1456 I ImeTracker: com.ghprotocol.app:20cfa38c: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 07:36:24.390  1499  1499 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 07:36:24.413  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40710) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:24.618  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40714) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:25.046  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40716) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:25.908  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40728) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:27.605  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40736) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:27.778   520   571 I AppsFilter: interaction: PackageSetting{263096a com.ghprotocol.app/10192} -> PackageSetting{8424456 com.google.android.contacts/10155} BLOCKED
10-25 07:36:30.997  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40738) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:37.784   520   571 I AppsFilter: interaction: PackageSetting{263096a com.ghprotocol.app/10192} -> PackageSetting{1abc16c com.google.android.contacts/10155} BLOCKED
10-25 07:36:37.909  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36848) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:36:51.477  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 58184) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:37:19.381  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39614) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:37:40.214  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:37:40.217  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.319  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.320  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.417  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.417  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.511  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.511  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.601  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.601  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.686  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.686  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.769  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.769  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.866  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.866  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.938  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:40.938  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.005  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.005  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.068  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.068  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.126  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.126  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.180  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.180  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.230  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.230  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.276  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.276  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.317  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.317  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.354  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.354  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.386  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.386  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.414  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.414  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.438  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.438  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.458  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.458  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.473  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.473  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.484  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.484  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.491  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.491  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.494  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.494  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:37:41.499  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:37:41.504  5614  5624 I .ghprotocol.app: Alloc concurrent copying GC freed 8362(482KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 6460KB/12MB, paused 11us,3us total 10.350ms
10-25 07:37:41.504  5614  5856 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.386ms
10-25 07:37:41.504  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.079  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:38:58.083  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.186  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.186  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.288  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.288  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.386  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.386  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.479  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.479  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.567  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.567  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.650  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.650  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.730  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.731  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.807  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.807  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.880  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.880  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.947  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:58.947  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.011  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.011  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.071  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.071  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.126  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.126  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.176  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.176  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.222  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.222  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.263  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.263  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.301  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.301  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.333  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.333  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.362  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.362  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.385  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.385  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.405  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.405  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.421  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.421  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.432  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.432  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.438  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.438  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.441  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.441  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:38:59.446  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:38:59.451  5614  5624 I .ghprotocol.app: Alloc concurrent copying GC freed 6538(421KB) AllocSpace objects, 4(80KB) LOS objects, 49% free, 6379KB/12MB, paused 11us,3us total 9.887ms
10-25 07:38:59.451  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:13.841  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41974) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:40:15.296  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41984) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:40:15.598  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:40:15.601  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.699  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.699  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.796  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.796  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.889  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.890  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.979  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:15.979  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.063  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.063  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.142  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.142  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.218  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.218  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.290  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.290  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.358  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.358  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.422  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.422  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.481  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.481  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.536  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.536  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.586  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.586  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.632  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.632  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.673  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.673  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.710  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.710  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.743  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.743  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.772  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.772  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.796  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.796  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.816  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.816  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.831  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.831  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.842  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.842  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.849  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.849  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.851  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.851  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:16.856  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:40:16.861  5614  5624 I .ghprotocol.app: Alloc concurrent copying GC freed 6476(414KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6379KB/12MB, paused 12us,3us total 10.095ms
10-25 07:40:16.861  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:40:18.293  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41988) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:40:24.289  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52932) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:40:36.278  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 53892) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:40:48.267  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34542) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:00.257  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41766) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:12.247  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54520) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:13.796  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54522) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:13.796  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54528) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:14.001  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54540) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:14.420  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54552) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:15.257  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54560) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:16.917  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54566) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:20.277  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54582) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:24.236  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60802) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:26.933  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60810) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:32.598  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:41:32.602  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.700  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.700  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.797  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.797  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.889  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.889  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.978  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:32.978  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.063  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.063  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.143  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.143  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.219  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.219  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.290  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.290  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.357  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.357  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.420  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.420  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.478  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.478  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.532  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.532  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.582  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.582  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.627  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.627  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.668  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.668  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.705  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.705  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.738  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.738  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.766  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.766  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.790  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.790  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.810  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.810  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.826  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.826  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.837  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.837  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.844  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.844  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.846  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.847  5614  5624 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:33.852  5614  5856 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:41:33.856  5614  5624 I .ghprotocol.app: Alloc concurrent copying GC freed 6884(440KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6369KB/12MB, paused 13us,3us total 9.610ms
10-25 07:41:33.856  5614  5856 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:41:36.226  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37236) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:40.245  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37242) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:41:48.215  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 40238) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:42:00.203  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39538) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:42:08.149  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 41332) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:42:12.193  5614  5856 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50498) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


