## gh-protocol E2E log — 2026-10-25T07:04:51Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T06:56:35Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 06:51 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 06:57 .
drwxr-xr-x 3 runner runner 4096 Oct 25 06:57 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 06:57 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 06:57 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2817
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
WARNING: cannnot unmap ptr 0x7f9a9f801000 as it is in the protected range from 0x7f999f800000 to 0x7f9a9fa00000
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
INFO         | Boot completed in 28194 ms
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
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:parseDebugLocalResources
> Task :app:javaPreCompileDebug
> Task :app:checkDebugAarMetadata
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeLibDexDebug
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugResources

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792911249127.json

BUILD SUCCESSFUL in 2m 8s
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
seeded cache: 37417 bytes, meta=1792911515577
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5834)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 3)
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5834   336   13916432 179336 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:37363  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:45063  [::]:*                  LISTEN     
tcp6       1     25 ::ffff:10.0.2.16:59046  ::ffff:142.251.150.:443 LAST_ACK   
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{ee28d4d u0 com.android.vpndialogs/.ConfirmDialog t-1 f}}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{2a15831 5834:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~A2WPwyZIZac8Pz3tK_c9xg==/com.ghprotocol.app-jwaYJyMQ2SJBEJuHj_QO1Q==/base.apk
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
      windows=[Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-6m5s482ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{2a15831 5834:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~A2WPwyZIZac8Pz3tK_c9xg==/com.ghprotocol.app-jwaYJyMQ2SJBEJuHj_QO1Q==/base.apk
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
      windows=[Window{fb19281 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-6m12s495ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@157520974
  deepestLastOrientationSource=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=98
  mCurrentFocus=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{a46d67c #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{448d917 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{1c6996 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{2ac3883 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{f641239 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{86c65c2 u0 StatusBar}
    mFocusedWindow=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
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
      Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {c4250000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=d112a4b InputMethod)/@0xb408772 - animation-leash of insets_animation)/@0xf8fd6c6 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{d112a4b u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=d112a4b InputMethod)/@0xb408772 - animation-leash of insets_animation)/@0xf8fd6c6
        mControlTarget=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false
      InsetsSourceProvider
        mSource=InsetsSource id=c4250006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{86c65c2 u0 StatusBar}
      InsetsSourceProvider
        mSource=InsetsSource id=c4250005 type=mandatorySystemGestures frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
--
        mWindowContainer=Window{86c65c2 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=86c65c2 StatusBar)/@0xed0e95d - animation-leash of insets_animation)/@0x6d2f687
        mControlTarget=Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false

--
        (multi-window) Task{4de2a00 #3 type=undefined}
        (multi-window) Task{f641239 #4 type=undefined}
        (fullscreen) Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{2a15831 5834:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6224
drwx------ 2 u0_a192 u0_a192    4096 2026-10-25 06:58 .
drwxrwxrwx 3 u0_a192 u0_a192    4096 2026-10-25 06:58 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-10-25 06:58 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-10-25 06:58 geosite.dat
-rw------- 1 u0_a192 u0_a192       0 2026-10-25 06:58 xray-err.log
-rw------- 1 u0_a192 u0_a192     506 2026-10-25 06:58 xray-out.log
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
Xray 26.10.21 (Xray, Penetrates Everything.) 1b1647c (go1.27.3 android/amd64)
A unified platform for anti-censorship.
2026/10/25 06:58:43.724318 [Info] infra/conf/serial: Reading config: &{Name:/data/user/0/com.ghprotocol.app/files/xray-config.json Format:json}
Failed to start: app/proxyman/inbound: failed to listen TCP on 53 > transport/internet: failed to listen on address: 127.0.0.1:53 > transport/internet/tcp: failed to listen tcp on 127.0.0.1:53 > listen tcp 127.0.0.1:53: bind: permission denied
runtime config (first 1400 bytes):
{"__Credits__":{"creator":"@patterniha","donate1":"USDT (BEP20): 0x76a768B53Ca77B43086946315f0BDF21156bF424","donate2":"USDT (TRC20): TU5gKvKqcXPn8itp1DouBCwcqGHMemBm8o","donate3":"TON (TON): UQAc-mZB3y7uxWHKiMmq0ORZEYgycWDWZ4V1k73HsXvTJx-i"},"remarks":"Serverless-v52-fragA","version":{"min":"26.6.27"},"log":{"loglevel":"warning","dnsLog":false,"access":"none"},"policy":{"levels":{"0":{"uplinkOnly":0,"downlinkOnly":0},"12":{"uplinkOnly":0,"downlinkOnly":0,"connIdle":12}}},"dns":{"hosts":{"geosite:category-ads-all":"#3","cloudflare-dns.com":"challenges.cloudflare.com"},"servers":[{"tag":"no-filter-dns","address":"https:\/\/cloudflare-dns.com\/dns-query","timeoutMs":12000,"finalQuery":true},{"tag":"domestic-dns","address":"localhost","domains":["domain:ir","geosite:private","geosite:category-ir","geosite:xai","geosite:openai","geosite:google-deepmind","geosite:anthropic","geosite:github","geosite:microsoft","geosite:golang","geosite:python","geosite:rust","full:challenges.cloudflare.com"],"timeoutMs":12000,"finalQuery":true}],"queryStrategy":"UseSystem","useSystemHosts":true,"serveStale":true},"inbounds":[{"tag":"mixed-in","port":10808,"protocol":"mixed","sniffing":{"enabled":true,"destOverride":["tls","http","quic"],"routeOnly":false},"settings":{"udp":true,"ip":"127.0.0.1"},"streamSettings":{"sockopt":{"tcpKeepAliveInterval":1,"tcpKeepAliveIdle":11}}},{"tag":"dns-in","protocol"core exit line:
10-25 06:58:44.286  5834  5931 W GhDiag  : xray exited rc=255
GhDiag (connect-flow trace):
--------- beginning of main
10-25 06:58:43.618  5834  5834 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:58:43.618  5834  5834 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:58:43.675  5834  5834 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:58:43.686  5834  5834 D GhDiag  : connect: config written bytes=5427 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:58:43.708  5834  5834 D GhDiag  : connect: core.start=true 
10-25 06:58:44.286  5834  5931 W GhDiag  : xray exited rc=255
10-25 06:58:53.884  5834  5834 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:58:53.934  5834  5834 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@cbce21f} — relay loop started
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
Visible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:58:43.527   543   610 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 06:58:43.618  5834  5834 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 06:58:43.618  5834  5834 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 06:58:43.640  5917  5917 W libxraycore.so: type=1400 audit(0.0:47): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 06:58:43.640  5917  5917 W libxraycore.so: type=1400 audit(0.0:48): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 06:58:43.640  5917  5917 W libxraycore.so: type=1400 audit(0.0:49): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 06:58:43.640  5917  5917 W libxraycore.so: type=1400 audit(0.0:50): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 06:58:43.675  5834  5834 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 06:58:43.686  5834  5834 D GhDiag  : connect: config written bytes=5427 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 06:58:43.688  5924  5924 W libxraycore.so: type=1400 audit(0.0:51): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 06:58:43.708  5834  5834 D GhDiag  : connect: core.start=true 
10-25 06:58:43.727   543   610 D CoreBackPreview: Window{ba3dd9e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@75f084c, mPriority=0, mIsAnimationCallback=false}
10-25 06:58:43.899   852   893 V WindowManagerShell: onTransitionReady android.os.BinderProxy@b6877cb: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity)/@0xdf8ee66 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity)/@0x484c5a7 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:58:43.899   852   893 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity)/@0xdf8ee66 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity)/@0x484c5a7 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:58:43.899   852   893 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity)/@0xdf8ee66 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity)/@0x484c5a7 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:58:43.904   543   560 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +370ms
10-25 06:58:43.905   543   560 V WindowManager: Sent Transition #7 createdAt=10-25 06:58:43.525 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=99346 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{407afa1 Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{eb00276 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:58:43.905   543   560 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{8bde523 u0 com.ghprotocol.app/.MainActivity)/@0x29a5d38 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{5b815b5 u0 com.ghprotocol.app/.MainActivity)/@0x468d59b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 06:58:44.071   852   893 V WindowManagerShell: Transition requested: android.os.BinderProxy@47be084 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=99751 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@13f006d} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b4294a2 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:58:44.286  5834  5931 W GhDiag  : xray exited rc=255
10-25 06:58:44.290   543  2324 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 06:58:44.291   543  2324 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 06:58:44.291   543  2324 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 06:58:44.859   543   560 V WindowManager: Sent Transition #8 createdAt=10-25 06:58:43.928 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=99751 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{407afa1 Task{4fc944a #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{88b88a4 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 06:58:45.212   543   594 I AppsFilter: interaction: PackageSetting{de5afe5 com.ghprotocol.app/10192} -> PackageSetting{eacac28 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 06:58:51.813  6047  6047 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 06:58:51.815  6047  6047 I AndroidRuntime: Using default boot image
10-25 06:58:51.815  6047  6047 I AndroidRuntime: Leaving lock profiling enabled
10-25 06:58:51.874  6047  6047 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 06:58:52.912  6047  6047 D AndroidRuntime: Shutting down VM
10-25 06:58:53.858   543  2321 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 06:58:53.884  5834  5834 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 06:58:53.933   543  1111 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 06:58:53.934  5834  5834 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@cbce21f} — relay loop started
10-25 06:58:54.028   543  1707 I ImeTracker: com.ghprotocol.app:aa7d3100: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 06:58:54.029   543  1707 I ImeTracker: com.ghprotocol.app:aa7d3100: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 06:58:54.068  1521  1521 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 06:58:54.104  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48898) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:58:54.326  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48900) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:58:54.488  5834  5843 I .ghprotocol.app: Background concurrent copying GC freed 121618(10MB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 7083KB/13MB, paused 24us,7us total 117.176ms
10-25 06:58:54.797  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 48914) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:58:55.697  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59202) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:58:57.488  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59210) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:58:57.583   543   594 I AppsFilter: interaction: PackageSetting{de5afe5 com.ghprotocol.app/10192} -> PackageSetting{dca955d com.google.android.contacts/10154} BLOCKED
10-25 06:59:01.165  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 59212) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:59:07.584   543   594 I AppsFilter: interaction: PackageSetting{de5afe5 com.ghprotocol.app/10192} -> PackageSetting{766b3da com.google.android.contacts/10154} BLOCKED
10-25 06:59:08.333  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49848) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:59:22.669  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38666) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 06:59:51.085  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 38656) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:01:07.983  5834  6075 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:01:07.984  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.093  5834  6075 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:01:08.093  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.202  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.202  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.312  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.312  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.419  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.419  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.530  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.530  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.633  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.633  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.732  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.732  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.827  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.827  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.920  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:08.920  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.006  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.006  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.089  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.089  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.170  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.170  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.250  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.250  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.325  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.325  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.396  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.396  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.464  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.464  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.529  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.529  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.590  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.590  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.649  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.649  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.704  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.704  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.757  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.757  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.807  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.807  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.853  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.853  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.897  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.897  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.938  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.938  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.976  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:09.976  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.011  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.011  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.043  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.043  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.070  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.071  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.096  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.096  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.118  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.118  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.136  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.136  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.151  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.151  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.162  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.162  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.171  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.171  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.176  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.176  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:01:10.184  5834  6075 I .ghprotocol.app: Alloc concurrent copying GC freed 6665(448KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6346KB/12MB, paused 9us,4us total 8.442ms
10-25 07:02:43.677  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42688) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:02:45.135  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43580) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:02:48.132  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43586) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:02:54.127  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 43602) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:06.116  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 54804) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:18.104  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 49778) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:30.092  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 50318) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:42.081  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46316) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:43.637  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46330) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:43.637  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46338) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:43.853  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46354) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:44.051  5834  6075 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:03:44.051  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.144  5834  6075 I .ghprotocol.app: Waiting for a blocking GC Alloc
10-25 07:03:44.145  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.237  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.237  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.305  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46356) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:44.331  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.331  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.422  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.422  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.512  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.512  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.598  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.598  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.679  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.679  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.772  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.772  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.849  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.849  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.924  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.924  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.997  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:44.997  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.065  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.065  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.129  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.129  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.165  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33362) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:45.191  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.191  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.250  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.250  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.305  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.305  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.357  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.357  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.404  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.404  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.450  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.450  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.491  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.491  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.529  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.529  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.564  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.564  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.595  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.595  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.624  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.624  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.649  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.649  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.671  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.672  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.690  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.690  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.706  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.706  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.718  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.718  5834  6075 I .ghprotocol.app: Starting a blocking GC Alloc
10-25 07:03:45.727  5834  6075 I .ghprotocol.app: Alloc concurrent copying GC freed 12603(965KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 6338KB/12MB, paused 9us,4us total 8.355ms
10-25 07:03:46.893  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33372) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:50.445  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33384) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:54.070  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 33400) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:03:57.357  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 46816) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:06.059  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39460) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:11.181  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 39466) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:18.298  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 42874) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:30.287  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 44436) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:39.853  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 47058) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)
10-25 07:04:42.277  5834  6075 W GhVpnTunnel: socks5 connect failed: failed to connect to /127.0.0.1 (port 10808) from /127.0.0.1 (port 47060) after 2000ms: isConnected failed: ECONNREFUSED (Connection refused)


