## gh-protocol E2E log — 2026-10-25T07:31:14Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T07:22:35Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 07:18 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 07:23 .
drwxr-xr-x 3 runner runner 4096 Oct 25 07:23 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 07:23 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 07:23 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2993
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
WARNING: cannnot unmap ptr 0x7faa42a01000 as it is in the protected range from 0x7fa942a00000 to 0x7faa42c00000
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
INFO         | Boot completed in 39358 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 53
ERROR        | Failed to bind to texture: invalid color buffer.
ERROR        | Failed to find ColorBuffer: 185
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
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:checkDebugAarMetadata
> Task :app:parseDebugLocalResources
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:mergeDebugResources
> Task :app:processDebugManifest
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugManifestForPackage
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugAssets
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:compressDebugAssets
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792912780529.json

BUILD SUCCESSFUL in 2m 44s
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
seeded cache: 37417 bytes, meta=1792913094769
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5416)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5416   336   14191376 177320 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:35227  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:37797  [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:45278  ::ffff:142.251.155.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{fb689c3 u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{6c5a263 5416:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~S_YOnEoNgHeZeAVbD6ubPQ==/com.ghprotocol.app-nkr-6KFgnN5hhlSkuyjTuw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.37 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m7s316ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{797c0c7 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{6c5a263 5416:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~S_YOnEoNgHeZeAVbD6ubPQ==/com.ghprotocol.app-nkr-6KFgnN5hhlSkuyjTuw==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.37 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.2 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{4f5c0b5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m14s353ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@88298990
  deepestLastOrientationSource=ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.37 fontWeightAdjustment=0}
  mLayoutSeq=92
  mCurrentFocus=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{797c0c7 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{ac7811c #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{3a13b9 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{22d4180 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{4e7242f #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{62c33c5 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{af4d8f3 u0 StatusBar}
    mFocusedWindow=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{9cbf57f u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=50160006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {50160000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=50160006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{af4d8f3 u0 StatusBar}
--
        mWindowContainer=Window{af4d8f3 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=af4d8f3 StatusBar)/@0x6614ed1 - animation-leash of insets_animation)/@0xa3933a6
        mControlTarget=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=b98e475 InputMethod)/@0xb0a2c7b - animation-leash of insets_animation)/@0x7bc1e7 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{b98e475 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=b98e475 InputMethod)/@0xb0a2c7b - animation-leash of insets_animation)/@0x7bc1e7
        mControlTarget=Window{a2ece38 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{ecaea3c #3 type=undefined}
        (multi-window) Task{62c33c5 #4 type=undefined}
        (fullscreen) Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{6c5a263 5416:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 07:25 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 07:25 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 07:25 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 07:25 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 07:25 xray-err.log
-rw------- 1 u0_a192 u0_a192     335 2026-10-25 07:25 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 07:25:03.693518 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: listen udp 127.0.0.1:5353: bind: address already in use
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 07:25:05.199  5416  5690 W GhDiag  : xray exited rc=255
GhDiag (connect-flow trace):
--------- beginning of main
10-25 07:25:03.018  5416  5416 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 07:25:03.019  5416  5416 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 07:25:03.236  5416  5416 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 07:25:03.270  5416  5416 D GhDiag  : connect: config written bytes=5429 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 07:25:03.454  5416  5416 D GhDiag  : connect: core.start=true 
10-25 07:25:05.199  5416  5690 W GhDiag  : xray exited rc=255
10-25 07:25:14.157  5416  5416 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 07:25:14.173  5416  5416 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@8608428} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
box/10132} BLOCKED
10-25 07:25:04.440   835   872 V WindowManagerShell: Transition requested: android.os.BinderProxy@13c780a TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=117422 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@50e587b} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{335698 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 07:25:04.501   521  2350 I ImeTracker: com.ghprotocol.app:3d62eb60: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 07:25:04.501   521  2350 I ImeTracker: com.ghprotocol.app:3d62eb60: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 07:25:04.536  1538  1538 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 07:25:05.009   521  2056 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 07:25:05.009   521  2056 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 07:25:05.009   521  2056 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 07:25:05.099  5416  5424 I .ghprotocol.app: Background concurrent copying GC freed 90288(4846KB) AllocSpace objects, 30(896KB) LOS objects, 49% free, 6370KB/12MB, paused 51us,8us total 251.977ms
10-25 07:25:05.178  5689  5689 W libxraycore.so: type=1400 audit(0.0:61): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=61276 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 07:25:05.199  5416  5690 W GhDiag  : xray exited rc=255
10-25 07:25:06.222   521   539 V WindowManager: Sent Transition #8 createdAt=10-25 07:25:04.163 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=117422 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{d032089 Task{943e6f4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{89bfa1a com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 07:25:11.435   521   573 I AppsFilter: interaction: PackageSetting{b0bf622 com.ghprotocol.app/10192} -> PackageSetting{4cf653b com.google.android.contacts/10154} BLOCKED
10-25 07:25:11.826  5845  5845 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 07:25:11.829  5845  5845 I AndroidRuntime: Using default boot image
10-25 07:25:11.829  5845  5845 I AndroidRuntime: Leaving lock profiling enabled
10-25 07:25:11.942  5845  5845 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 07:25:13.046  5845  5845 D AndroidRuntime: Shutting down VM
10-25 07:25:14.117   521  2044 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 07:25:14.157  5416  5416 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 07:25:14.173   521  1882 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 07:25:14.173  5416  5416 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@8608428} — relay loop started
10-25 07:25:14.371   521  2055 I ImeTracker: com.ghprotocol.app:da940c1b: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 07:25:14.373   521  2055 I ImeTracker: com.ghprotocol.app:da940c1b: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 07:25:14.375  1538  1538 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 07:25:14.450  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50878) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:14.643  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50884) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:15.067  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50900) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:15.931  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50906) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:17.627  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33064) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:19.196  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33080) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:20.219  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33082) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:21.147  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33096) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:21.486   521   573 I AppsFilter: interaction: PackageSetting{b0bf622 com.ghprotocol.app/10192} -> PackageSetting{18abbf6 com.google.android.contacts/10154} BLOCKED
10-25 07:25:22.235  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33108) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:26.267  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33120) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:28.059  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56784) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:34.459  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56786) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:41.627  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37306) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:25:52.666   521   573 I AppsFilter: interaction: PackageSetting{b0bf622 com.ghprotocol.app/10192} -> PackageSetting{a700994 com.google.android.contacts/10154} BLOCKED
10-25 07:26:02.683   521   573 I AppsFilter: interaction: PackageSetting{b0bf622 com.ghprotocol.app/10192} -> PackageSetting{1ca2c17 com.google.android.contacts/10154} BLOCKED
10-25 07:26:10.043  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 51382) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:26:55.477  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:26:55.480  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.641  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.641  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.768  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.769  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.890  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:55.890  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.006  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.006  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.118  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.118  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.221  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.221  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.320  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.320  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.414  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.414  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.501  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.501  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.581  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.581  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.657  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.657  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.726  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.726  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.788  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.788  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.845  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.845  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.895  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.895  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.941  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.941  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.980  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:56.980  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.012  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.013  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.039  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.039  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.061  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.061  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.076  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.076  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.085  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.085  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.088  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.088  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.088  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:26:57.091  5416  5426 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:26:57.091  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.091  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.092  5416  5426 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:26:57.105  5416  5881 I .ghprotocol.app: Alloc concurrent copying GC freed 5776(230KB) AllocSpace objects, 16(320KB) LOS objects, 49% free, 6362KB/12MB, paused 20us,7us total 13.748ms
10-25 07:26:57.106  5416  5426 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 14.379ms
10-25 07:26:57.106  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:26:57.118  5416  5426 I .ghprotocol.app: Alloc concurrent copying GC freed 5401(211KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6599KB/12MB, paused 80us,13us total 12.050ms
10-25 07:28:52.882  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:28:52.886  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.040  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.040  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.191  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.191  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.346  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.346  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.483  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.484  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.617  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.617  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.745  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.745  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.929  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.930  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:53.937  5416  5881 I .ghprotocol.app: Alloc young concurrent copying GC freed 58236(5135KB) AllocSpace objects, 0(0B) LOS objects, 51% free, 6343KB/12MB, paused 31us,5us total 7.164ms
10-25 07:28:54.137  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.137  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.301  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.301  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.471  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.471  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.479  5416  5881 I .ghprotocol.app: Alloc young concurrent copying GC freed 49500(4367KB) AllocSpace objects, 0(0B) LOS objects, 51% free, 6344KB/12MB, paused 22us,6us total 8.778ms
10-25 07:28:54.595  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.595  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.703  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.703  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.714  5416  5881 I .ghprotocol.app: Alloc young concurrent copying GC freed 43676(3855KB) AllocSpace objects, 0(0B) LOS objects, 51% free, 6345KB/12MB, paused 122us,8us total 11.577ms
10-25 07:28:54.889  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:54.889  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.001  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.001  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.092  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.092  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.189  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.189  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.255  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.255  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.311  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.311  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.362  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.362  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.406  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.406  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.445  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.445  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.478  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.478  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.505  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.505  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.526  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.527  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.541  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.541  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.550  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.550  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.553  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.553  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.554  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:28:55.557  5416  5426 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:28:55.557  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:28:55.557  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:28:55.567  5416  5426 I .ghprotocol.app: Alloc concurrent copying GC freed 3749(171KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6180KB/12MB, paused 12us,10us total 10.216ms
10-25 07:28:55.567  5416  5881 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 13.213ms
10-25 07:28:55.567  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:29:03.083  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46918) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:04.541  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46922) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:07.650  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 57162) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:13.646  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 57174) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:25.636  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52834) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:37.627  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33908) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:29:49.617  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37408) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:01.608  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48010) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:03.025  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48020) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:03.026  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48026) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:03.231  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48032) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:03.643  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48038) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:04.475  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48048) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:06.139  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48064) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:09.659  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 55994) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:13.598  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56000) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:16.315  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 56014) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:25.588  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 36440) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:29.627  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49420) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:37.579  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49432) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:38.183  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:30:38.186  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.317  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.317  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.445  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.445  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.567  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.567  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.684  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.684  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.796  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.803  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.912  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:38.912  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.010  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.010  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.102  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.102  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.189  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.189  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.269  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.269  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.343  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.343  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.413  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.413  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.475  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.475  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.532  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.532  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.583  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.583  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.628  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.628  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.668  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.668  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.701  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.701  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.729  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.729  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.750  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.750  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.765  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.765  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.774  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.774  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.777  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.777  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.777  5416  5881 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:30:39.780  5416  5426 I .ghprotocol.app: Forcing collection of SoftReferences for 24B allocation
10-25 07:30:39.780  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.780  5416  5881 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.780  5416  5426 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:30:39.792  5416  5881 I .ghprotocol.app: Alloc concurrent copying GC freed 3800(166KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6182KB/12MB, paused 17us,4us total 11.784ms
10-25 07:30:39.792  5416  5426 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 12.013ms
10-25 07:30:39.792  5416  5426 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:30:39.802  5416  5426 I .ghprotocol.app: Alloc concurrent copying GC freed 402(47KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6535KB/12MB, paused 49us,9us total 10.299ms
10-25 07:30:49.568  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 32992) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:30:56.763  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33008) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:31:01.559  5416  5881 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42594) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


