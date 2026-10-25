## gh-protocol E2E log — 2026-10-25T06:52:31Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T06:44:04Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 06:40 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 06:44 .
drwxr-xr-x 3 runner runner 4096 Oct 25 06:44 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 06:44 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 06:44 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3047
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
WARNING: cannnot unmap ptr 0x7f25a4e01000 as it is in the protected range from 0x7f24a4e00000 to 0x7f25a5000000
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
INFO         | Boot completed in 37564 ms
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
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:compressDebugAssets
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:mergeDebugNativeLibs
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792910483743.json

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
seeded cache: 37417 bytes, meta=1792910771990
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5361)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5361   338   13735740 177292 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:43619  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:40473  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:41118  ::ffff:142.251.155.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{ff277ab u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{e74b363 5361:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~1c_xSkwX01Nw0uVLbymeMw==/com.ghprotocol.app-spmVFIAu1li7u01r_nF3aQ==/base.apk
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
      windows=[Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m7s21ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{5c7c1c7 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{e74b363 5361:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~1c_xSkwX01Nw0uVLbymeMw==/com.ghprotocol.app-spmVFIAu1li7u01r_nF3aQ==/base.apk
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
      windows=[Window{7780d87 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m13s934ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@180064688
  deepestLastOrientationSource=ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=93
  mCurrentFocus=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{5c7c1c7 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{1ceb7ae #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{8b64da5 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{7e7bf9c u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{ce36f30 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{a67912e #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{84cfd4a u0 StatusBar}
    mFocusedWindow=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=b750006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {b750000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=b750006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{84cfd4a u0 StatusBar}
--
        mWindowContainer=Window{84cfd4a u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=84cfd4a StatusBar)/@0xe5a416 - animation-leash of insets_animation)/@0xd89c125
        mControlTarget=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=dd20cdd InputMethod)/@0x89a4f23 - animation-leash of insets_animation)/@0x41eb2fa mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{dd20cdd u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=dd20cdd InputMethod)/@0x89a4f23 - animation-leash of insets_animation)/@0x41eb2fa
        mControlTarget=Window{a56fb0e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{7d727a9 #3 type=undefined}
        (multi-window) Task{a67912e #4 type=undefined}
        (fullscreen) Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{e74b363 5361:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 06:46 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 06:46 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 06:46 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 06:46 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 06:46 xray-err.log
-rw------- 1 u0_a192 u0_a192     537 2026-10-25 06:46 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 06:46:20.615372 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: main: failed to load config files: [/data/user/0/com.ghprotocol.app/files/xray-config.json] > infra/conf: failed to build inbound config with tag dns-in > infra/conf: failed to load inbound detour config for protocol dns > infra/conf: unknown config id: dns
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 06:46:20.665  5361  5594 W GhDiag  : xray exited rc=23
GhDiag (connect-flow trace):
--------- beginning of main
10-25 06:46:20.234  5361  5361 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:46:20.234  5361  5361 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:46:20.402  5361  5361 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:46:20.423  5361  5361 D GhDiag  : connect: config written bytes=5272 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:46:20.580  5361  5361 D GhDiag  : connect: core.start=true 
10-25 06:46:20.665  5361  5594 W GhDiag  : xray exited rc=23
10-25 06:46:31.370  5361  5361 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:46:31.440  5361  5361 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@5cad7fc} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
.911   522   540 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +864ms
10-25 06:46:20.911   522   540 V WindowManager: Sent Transition #7 createdAt=10-25 06:46:20.040 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=109228 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{666749a Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d0eebda com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:46:20.911   522   540 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{712ffe2 u0 com.ghprotocol.app/.MainActivity)/@0x51566fc sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{5c7c1c7 u0 com.ghprotocol.app/.MainActivity)/@0x78e9bef sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:46:21.166   833   874 V WindowManagerShell: Transition requested: android.os.BinderProxy@b6ac73 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=110145 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@a44a730} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{94bffa9 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:46:21.183   522   913 I ImeTracker: com.ghprotocol.app:9c346c25: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 06:46:21.183   522   913 I ImeTracker: com.ghprotocol.app:9c346c25: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:46:21.197  1513  1513 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:46:21.261   522   537 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 06:46:21.267   522   537 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 06:46:21.267   522   537 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 06:46:21.957   522   540 V WindowManager: Sent Transition #8 createdAt=10-25 06:46:20.950 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=110145 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{666749a Task{a0253f4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{1787b09 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:46:22.467  5361  5370 I .ghprotocol.app: Background concurrent copying GC freed 100390(5251KB) AllocSpace objects, 30(896KB) LOS objects, 49% free, 6578KB/12MB, paused 41us,2.817ms total 133.419ms
10-25 06:46:26.361   522   576 I AppsFilter: interaction: PackageSetting{6b4e65e com.ghprotocol.app/10192} -> PackageSetting{1e4c37f com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 06:46:26.361   522   576 I AppsFilter: interaction: PackageSetting{6b4e65e com.ghprotocol.app/10192} -> PackageSetting{5321f4c com.google.android.as/10125} BLOCKED
10-25 06:46:28.606  5779  5779 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 06:46:28.611  5779  5779 I AndroidRuntime: Using default boot image
10-25 06:46:28.611  5779  5779 I AndroidRuntime: Leaving lock profiling enabled
10-25 06:46:28.877  5779  5779 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 06:46:30.007  5779  5779 D AndroidRuntime: Shutting down VM
10-25 06:46:30.309   522   576 I AppsFilter: interaction: PackageSetting{6b4e65e com.ghprotocol.app/10192} -> PackageSetting{c1ca432 com.google.android.contacts/10154} BLOCKED
10-25 06:46:31.272   522  1161 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 06:46:31.370  5361  5361 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:46:31.440   522  2331 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 06:46:31.440  5361  5361 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@5cad7fc} — relay loop started
10-25 06:46:31.453   522  1255 I ImeTracker: com.ghprotocol.app:1fc3c3ab: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 06:46:31.453   522  1255 I ImeTracker: com.ghprotocol.app:1fc3c3ab: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:46:31.519  1513  1513 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:46:31.785  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45404) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:31.975  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45412) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:32.410  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45424) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:33.242  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45432) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:34.907  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45444) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:37.307  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45448) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:38.298  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45454) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:38.330  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45464) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:40.347  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 45466) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:44.442  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 35894) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:44.954  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 35906) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:52.634  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48540) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:46:58.266  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48552) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:47:10.719   522   576 I AppsFilter: interaction: PackageSetting{6b4e65e com.ghprotocol.app/10192} -> PackageSetting{f140c71 com.google.android.contacts/10154} BLOCKED
10-25 06:47:20.729   522   576 I AppsFilter: interaction: PackageSetting{6b4e65e com.ghprotocol.app/10192} -> PackageSetting{5217f60 com.google.android.contacts/10154} BLOCKED
10-25 06:47:25.914  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 52036) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:48:17.690  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:48:17.694  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:17.827  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:17.827  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:17.959  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:17.959  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.086  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.086  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.207  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.207  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.321  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.321  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.430  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.430  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.531  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.532  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.627  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.627  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.717  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.717  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.802  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.802  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.880  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.880  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.952  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:18.952  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.019  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.019  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.085  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.085  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.141  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.141  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.191  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.191  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.236  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.236  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.274  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.274  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.308  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.308  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.334  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.334  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.355  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.355  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.369  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.369  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.379  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.379  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.382  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.382  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:48:19.392  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:48:19.397  5361  5372 I .ghprotocol.app: Alloc concurrent copying GC freed 8196(475KB) AllocSpace objects, 8(160KB) LOS objects, 49% free, 6557KB/12MB, paused 46us,4us total 14.944ms
10-25 06:48:19.397  5361  5824 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.359ms
10-25 06:48:19.397  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.399  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:50:06.403  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.544  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.544  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.683  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.683  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.815  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.815  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.942  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:06.942  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.061  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.061  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.176  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.176  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.285  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.285  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.387  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.387  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.484  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.484  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.575  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.575  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.660  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.660  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.739  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.739  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.812  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.812  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.878  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.878  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.939  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.939  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.994  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:07.994  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.043  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.043  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.086  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.086  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.123  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.123  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.155  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.155  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.181  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.181  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.201  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.202  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.216  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.216  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.224  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.224  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.227  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.227  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:08.234  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:50:08.239  5361  5372 I .ghprotocol.app: Alloc concurrent copying GC freed 6576(418KB) AllocSpace objects, 8(160KB) LOS objects, 49% free, 6394KB/12MB, paused 14us,3us total 12.134ms
10-25 06:50:08.239  5361  5824 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.423ms
10-25 06:50:08.240  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:50:20.282  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37532) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:50:21.740  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49242) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:50:24.738  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49256) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:50:30.872  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49260) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:50:42.863  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 34424) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:50:55.242  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38948) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:07.231  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49984) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:19.221  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60860) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:20.242  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60868) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:20.243  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60876) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:20.447  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60880) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:20.858  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60896) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:21.691  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37896) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:23.354  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37910) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:26.810  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37912) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:31.211  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37922) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:33.467  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 32854) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:43.201  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60350) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:46.778  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 60358) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:51:52.496  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:51:52.499  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.633  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.633  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.766  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.766  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.891  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:52.891  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.010  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.010  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.123  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.123  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.231  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.231  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.332  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.332  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.428  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.428  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.520  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.520  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.605  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.605  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.684  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.684  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.756  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.756  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.823  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.823  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.884  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.884  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.940  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.940  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.989  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:53.989  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.033  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.033  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.071  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.071  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.102  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.102  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.128  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.128  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.149  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.149  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.163  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.163  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.171  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.171  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.174  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.174  5361  5372 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:54.181  5361  5824 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 06:51:54.186  5361  5372 I .ghprotocol.app: Alloc concurrent copying GC freed 6752(444KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6375KB/12MB, paused 18us,3us total 11.935ms
10-25 06:51:54.186  5361  5824 I .ghprotocol.app: WaitForGcToComplete blocked Alloc on Alloc for 5.113ms
10-25 06:51:54.186  5361  5824 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 06:51:55.190  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 37480) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:52:07.180  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59810) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:52:14.682  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46600) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:52:19.170  5361  5824 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46616) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


