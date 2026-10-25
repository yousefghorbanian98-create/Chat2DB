## gh-protocol E2E log — 2026-10-25T06:40:49Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T06:32:13Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 06:28 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 06:32 .
drwxr-xr-x 3 runner runner 4096 Oct 25 06:32 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 06:32 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 06:32 gh_test.ini

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
ERROR        | Unable to connect to adb daemon on port: 5037
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3048
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
WARNING: cannnot unmap ptr 0x7f6d04401000 as it is in the protected range from 0x7f6c04400000 to 0x7f6d04600000
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
INFO         | Boot completed in 38411 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 180
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
> Task :app:mergeDebugShaders
> Task :app:packageDebugResources
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugResources

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeLibDexDebug
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792909770171.json

BUILD SUCCESSFUL in 2m 40s
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
seeded cache: 37417 bytes, meta=1792910070160
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5338)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5338   336   13772628 176416 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:40765  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:43217  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:35178  ::ffff:142.251.157.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{b9d8dc1 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{6c6456 5338:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~hbQR4B7JBz2Wd7t4mLGpWw==/com.ghprotocol.app-9SQulb3oQ_jkBX_qooWdgw==/base.apk
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
      windows=[Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m7s87ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{c7c398a u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{6c6456 5338:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~hbQR4B7JBz2Wd7t4mLGpWw==/com.ghprotocol.app-9SQulb3oQ_jkBX_qooWdgw==/base.apk
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
      windows=[Window{82fc6ba u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m13s868ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@158479076
  deepestLastOrientationSource=ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=95
  mCurrentFocus=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{c7c398a u0 com.ghprotocol.app/.MainActivity t8}
      * Task{2981e02 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{feb3a1e #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{64d1e59 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{c472c4 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{6050fa9 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{ef71889 u0 StatusBar}
    mFocusedWindow=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=54950006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {54950000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=54950006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{ef71889 u0 StatusBar}
--
        mWindowContainer=Window{ef71889 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=ef71889 StatusBar)/@0xb2fb445 - animation-leash of insets_animation)/@0x61fca72
        mControlTarget=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=9f55958 InputMethod)/@0xaecab96 - animation-leash of insets_animation)/@0x1641ec3 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{9f55958 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=9f55958 InputMethod)/@0xaecab96 - animation-leash of insets_animation)/@0x1641ec3
        mControlTarget=Window{a08a3a5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{634c5ad #3 type=undefined}
        (multi-window) Task{6050fa9 #4 type=undefined}
        (fullscreen) Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{6c6456 5338:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 06:34 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 06:34 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 06:34 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 06:34 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 06:34 xray-err.log
-rw------- 1 u0_a192 u0_a192     537 2026-10-25 06:34 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 06:34:38.929823 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: main: failed to load config files: [/data/user/0/com.ghprotocol.app/files/xray-config.json] > infra/conf: failed to build inbound config with tag dns-in > infra/conf: failed to load inbound detour config for protocol dns > infra/conf: unknown config id: dns
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 06:34:38.965  5338  5591 W GhDiag  : xray exited rc=23
GhDiag (connect-flow trace):
--------- beginning of main
10-25 06:34:38.402  5338  5338 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:34:38.402  5338  5338 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:34:38.665  5338  5338 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:34:38.685  5338  5338 D GhDiag  : connect: config written bytes=5272 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:34:38.834  5338  5338 D GhDiag  : connect: core.start=true 
10-25 06:34:38.965  5338  5591 W GhDiag  : xray exited rc=23
10-25 06:34:49.665  5338  5338 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:34:49.763  5338  5338 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@3d92a6e} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
 ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +980ms
10-25 06:34:39.161   523   540 V WindowManager: Sent Transition #7 createdAt=10-25 06:34:38.178 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=109805 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ca8e9c7 Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{f38a25d com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:34:39.161   523   540 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{8ad8e6e u0 com.ghprotocol.app/.MainActivity)/@0x4ef5b07 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{c7c398a u0 com.ghprotocol.app/.MainActivity)/@0x184fd46 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:34:39.415   838   874 V WindowManagerShell: Transition requested: android.os.BinderProxy@7e514da TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=110797 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@3807d0b} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{550c7e8 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:34:39.449   523   592 I ImeTracker: com.ghprotocol.app:629ff389: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 06:34:39.449   523   592 I ImeTracker: com.ghprotocol.app:629ff389: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:34:39.481  1534  1534 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:34:39.504   523  2146 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 06:34:39.506   523  2146 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 06:34:39.506   523  2146 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 06:34:40.028   523   540 V WindowManager: Sent Transition #8 createdAt=10-25 06:34:39.170 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=110797 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{ca8e9c7 Task{528bbfb #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2bb13e4 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:34:40.515  5338  5348 I .ghprotocol.app: Background concurrent copying GC freed 106519(5441KB) AllocSpace objects, 30(896KB) LOS objects, 49% free, 6467KB/12MB, paused 41us,9us total 120.368ms
10-25 06:34:44.752   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{400b63f com.google.android.as/10125} BLOCKED
10-25 06:34:44.752   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{f8efb0c com.google.android.contacts/10156} BLOCKED
10-25 06:34:45.870   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{b35e74a com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 06:34:46.774  5781  5781 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 06:34:46.783  5781  5781 I AndroidRuntime: Using default boot image
10-25 06:34:46.783  5781  5781 I AndroidRuntime: Leaving lock profiling enabled
10-25 06:34:46.993  5781  5781 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 06:34:48.151  5781  5781 D AndroidRuntime: Shutting down VM
10-25 06:34:49.435   523  1734 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 06:34:49.665  5338  5338 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:34:49.756   523  1894 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 06:34:49.763  5338  5338 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@3d92a6e} — relay loop started
10-25 06:34:49.880   523  1744 I ImeTracker: com.ghprotocol.app:d92b00ec: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 06:34:49.880   523  1744 I ImeTracker: com.ghprotocol.app:d92b00ec: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:34:49.881  1534  1534 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:34:49.983  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45368) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:50.194  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45380) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:50.615  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45396) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:51.480  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45406) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:53.176  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45422) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:55.604   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{6aaf50a com.google.android.contacts/10156} BLOCKED
10-25 06:34:56.344  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45424) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:56.632  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45430) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:57.368  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45442) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:34:59.383  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33692) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:35:03.544  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33698) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:35:03.545  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33700) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:35:11.739  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55896) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:35:17.112  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55912) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:35:29.788   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{60f8110 com.google.android.contacts/10156} BLOCKED
10-25 06:35:39.798   523   574 I AppsFilter: interaction: PackageSetting{13ed106 com.ghprotocol.app/10192} -> PackageSetting{27bfc0e com.google.android.contacts/10156} BLOCKED
10-25 06:35:45.528  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 58464) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:36:36.333  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:36:36.337  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.481  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.481  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.619  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.620  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.753  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.753  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.878  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.878  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.996  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:36.996  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.111  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.111  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.219  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.219  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.321  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.321  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.417  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.417  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.507  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.507  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.590  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.590  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.669  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.669  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.740  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.740  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.805  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.805  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.862  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.862  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.913  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.913  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.959  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.959  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.999  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:37.999  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.032  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.032  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.060  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.060  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.084  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.084  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.100  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.100  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.108  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.108  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.111  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.111  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:36:38.118  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:36:38.124  5338  5350 I .ghprotocol.app: Alloc concurrent copying GC freed 8488(482KB) AllocSpace objects, 16(320KB) LOS objects, 49% free, 6365KB/12MB, paused 20us,4us total 12.109ms
10-25 06:36:38.124  5338  5815 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.175ms
10-25 06:36:38.124  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.425  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:38:26.431  5338  5815 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Background for 5.143ms
10-25 06:38:26.431  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.569  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.569  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.703  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.703  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.831  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.831  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.953  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:26.953  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.070  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.071  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.181  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.181  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.285  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.285  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.383  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.383  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.477  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.477  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.565  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.565  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.648  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.648  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.723  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.723  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.793  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.793  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.858  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.858  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.916  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.916  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.976  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:27.976  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.022  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.022  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.062  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.062  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.096  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.096  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.123  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.123  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.145  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.145  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.160  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.160  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.168  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.168  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.171  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.171  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:28.178  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:38:28.183  5338  5350 I .ghprotocol.app: Alloc concurrent copying GC freed 6315(402KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6364KB/12MB, paused 19us,3us total 11.495ms
10-25 06:38:28.183  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:38:38.452  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 47114) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:38:39.910  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36278) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:38:42.908  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36294) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:38:49.289  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43448) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:01.279  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36680) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:13.269  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55796) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:25.257  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 44470) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:37.248  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43418) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:38.411  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43428) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:38.412  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43432) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:38.620  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43434) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:39.063  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43446) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:39.928  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45226) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:41.624  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45238) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:45.143  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45246) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:49.238  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59910) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:39:52.056  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59918) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:01.227  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 51952) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:05.623  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 51964) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:13.216  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55944) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:15.780  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:40:15.784  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:15.922  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:15.922  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.059  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.059  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.191  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.191  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.317  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.317  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.434  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.434  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.547  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.547  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.654  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.654  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.754  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.754  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.848  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.848  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.934  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:16.934  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.016  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.016  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.093  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.093  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.164  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.164  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.228  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.228  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.288  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.288  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.340  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.340  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.385  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.385  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.425  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.425  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.458  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.458  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.486  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.486  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.507  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.507  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.522  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.522  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.532  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.532  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.535  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.535  5338  5350 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:17.545  5338  5815 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:40:17.550  5338  5350 I .ghprotocol.app: Alloc concurrent copying GC freed 6617(427KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6355KB/12MB, paused 30us,3us total 15.476ms
10-25 06:40:17.550  5338  5815 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.252ms
10-25 06:40:17.550  5338  5815 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:40:25.206  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39376) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:34.296  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38250) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:40:37.196  5338  5815 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38254) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


