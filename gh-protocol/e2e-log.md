## gh-protocol E2E log — 2026-10-24T21:43:45Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-24T21:34:38Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 24 21:30 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 1.7G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 24 21:35 .
drwxr-xr-x 3 runner runner 4096 Oct 24 21:35 ..
drwxr-xr-x 3 runner runner 4096 Oct 24 21:35 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 24 21:35 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2805
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
WARNING: cannnot unmap ptr 0x7fb2b3a01000 as it is in the protected range from 0x7fb1b3a00000 to 0x7fb2b3c00000
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
INFO         | Boot completed in 25262 ms
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
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:checkDebugAarMetadata
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:checkDebugDuplicateClasses
> Task :app:validateSigningDebug
> Task :app:compressDebugAssets
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792877539128.json

BUILD SUCCESSFUL in 2m 18s
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
seeded cache: 37417 bytes, meta=1792877792552
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2343)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a141       2343   326   13574716 174424 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:54844  ::ffff:172.217.114.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{8a8beaa 2343:com.ghprotocol.app/u0a141}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.apk
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
      windows=[Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-7m3s161ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=false
    * Hist  #0: ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{8a8beaa 2343:com.ghprotocol.app/u0a141}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.apk
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
      windows=[Window{f78898 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-7m10s475ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=true mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@199692868
  deepestLastOrientationSource=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.34 fontWeightAdjustment=0}
  mLayoutSeq=66
  mCurrentFocus=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  Display areas in top down Z order:
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}
      mLastFocusedRootTask=Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity t8}
      * Task{da77c62 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{a22e93 #7 type=home I=com.android.launcher3/.uioverrides.QuickstepLauncher U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{f6ff782 u0 com.android.launcher3/.uioverrides.QuickstepLauncher t7}
      * Task{fae3574 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{61522e3 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{39a2636 u0 StatusBar}
    mFocusedWindow=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=688c0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(540, 2400) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {688c0000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=688c0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{39a2636 u0 StatusBar}
--
        mWindowContainer=Window{39a2636 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=39a2636 StatusBar)/@0xe1ae1d3 - animation-leash of insets_animation)/@0x372af59
        mControlTarget=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(540, 2400 - 540, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=756c522 InputMethod)/@0xc8d6570 - animation-leash of insets_animation)/@0x117f71e mInitiallyVisible=false mSurfacePosition=Point(540, 2400) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{756c522 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=756c522 InputMethod)/@0xc8d6570 - animation-leash of insets_animation)/@0x117f71e
        mControlTarget=Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{9dfcb12 #3 type=undefined}
        (multi-window) Task{61522e3 #4 type=undefined}
        (fullscreen) Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{8a8beaa 2343:com.ghprotocol.app/u0a141}]
  NumNonAppVisibleWindowUidMap:[ 10117:1]
app filesDir/xray:
total 79624
drwx------ 2 u0_a141 u0_a141     4096 2026-10-24 21:36 .
drwxrwxrwx 3 u0_a141 u0_a141     4096 2026-10-24 21:36 ..
-rwx--x--x 1 u0_a141 u0_a141 38872056 2026-10-24 21:36 Xray
-rw------- 1 u0_a141 u0_a141 36282168 2026-10-24 21:36 Xray-arm64-v8a
-rw------- 1 u0_a141 u0_a141  3977011 2026-10-24 21:36 geoip.dat
-rw------- 1 u0_a141 u0_a141  2358471 2026-10-24 21:36 geosite.dat
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-24 21:36:40.616  2343  2343 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-24 21:36:40.617  2343  2343 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-24 21:36:40.960  2343  2343 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-24 21:36:40.960  2343  2343 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
intent user: UserHandle{0}
10-24 21:35:33.346  1008  1008 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-24 21:35:33.349  1008  1298 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-24 21:35:33.349  1008  1008 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-24 21:35:33.351  1008  1298 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-24 21:35:35.179   508   560 I AppsFilter: interaction: PackageSetting{cafb088 com.ghprotocol.app/10141} -> PackageSetting{fc7ca21 com.android.camera2/10104} BLOCKED
10-24 21:35:35.179   508   560 I AppsFilter: interaction: PackageSetting{cafb088 com.ghprotocol.app/10141} -> PackageSetting{e2d4e46 com.android.calendar/10099} BLOCKED
10-24 21:35:35.179   508   560 I AppsFilter: interaction: PackageSetting{cafb088 com.ghprotocol.app/10141} -> PackageSetting{747d807 com.android.rkpdapp/10130} BLOCKED
10-24 21:35:35.179   508   560 I AppsFilter: interaction: PackageSetting{cafb088 com.ghprotocol.app/10141} -> PackageSetting{9d34d34 com.android.inputmethod.latin/10109} BLOCKED
10-24 21:35:35.179   508   560 I AppsFilter: interaction: PackageSetting{cafb088 com.ghprotocol.app/10141} -> PackageSetting{ab5e75d com.android.cellbroadcastreceiver.module/10119} BLOCKED
10-24 21:36:32.440   508  1315 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-24 21:36:32.442   508  1315 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 21:36:32.443   799   832 V WindowManagerShell: Transition requested: android.os.BinderProxy@e35c470 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=87368 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@d5ef3e9} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{ef5086e com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:36:32.465   508  1315 D CoreBackPreview: Window{6fc3a4d u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@b1c5213, mPriority=0, mIsAnimationCallback=false}
10-24 21:36:32.477   508   537 I ActivityManager: Start proc 2343:com.ghprotocol.app/u0a141 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-24 21:36:32.534  2343  2343 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-24 21:36:32.552  2343  2343 I .ghprotocol.app: Using CollectorTypeCC GC.
10-24 21:36:32.553  2343  2343 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-24 21:36:32.553  2343  2343 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-24 21:36:32.697   508   525 V WindowManager: Sent Transition #6 createdAt=10-24 21:36:32.435 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=87368 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c27f568 Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{395d81 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:36:32.697   508   525 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{c27f568 Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x197234e sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{5b04e26 Task{da77c62 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xb21fa65 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:36:32.733  2343  2343 W ziparchive: Unable to open '/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.dm': No such file or directory
10-24 21:36:32.733  2343  2343 W ziparchive: Unable to open '/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.dm': No such file or directory
10-24 21:36:32.948  2343  2343 D nativeloader: Configuring clns-6 for other apk /data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/lib/x86_64:/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-24 21:36:32.954  2343  2343 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-24 21:36:32.954  2343  2343 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: and incorrect proguard optimizations.
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:36:33.198  2343  2343 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 21:36:33.199  2343  2343 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 21:36:33.233   508   522 D CoreBackPreview: Window{f78898 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@95d8529, mPriority=0, mIsAnimationCallback=false}
10-24 21:36:33.745   508   525 W ziparchive: Unable to open '/data/app/~~qroX5DjK3zTAE9cTJT9dEw==/com.ghprotocol.app-YPgR8V7hPFTiW63C4lgS8g==/base.dm': No such file or directory
10-24 21:36:33.746   508   525 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s312ms
10-24 21:36:33.764   508   522 I ImeTracker: com.ghprotocol.app:ebd2ba56: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-24 21:36:33.764   508   522 I ImeTracker: com.ghprotocol.app:ebd2ba56: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-24 21:36:33.769   508   522 D CoreBackPreview: Window{6fc3a4d u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-24 21:36:33.769   508  1982 W InputManager-JNI: Input channel object '6fc3a4d Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 21:36:38.320  2343  2390 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-24 21:36:40.484   508   522 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 21:36:40.484   799   832 V WindowManagerShell: Transition requested: android.os.BinderProxy@7f100da TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=95408 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@27bf90b} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{e2c93e8 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:36:40.616  2343  2343 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-24 21:36:40.617  2343  2343 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-24 21:36:40.950  2404  2404 W .ghprotocol.app: type=1400 audit(0.0:15): avc:  granted  { execute } for  name="Xray" dev="dm-38" ino=131276 scontext=u:r:untrusted_app:s0:c141,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c141,c256,c512,c768 tclass=file app=com.ghprotocol.app
10-24 21:36:40.950  2404  2404 W .ghprotocol.app: type=1400 audit(0.0:16): avc:  denied  { execute_no_trans } for  path="/data/data/com.ghprotocol.app/files/xray/Xray" dev="dm-38" ino=131276 scontext=u:r:untrusted_app:s0:c141,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c141,c256,c512,c768 tclass=file permissive=0 app=com.ghprotocol.app
10-24 21:36:40.960  2343  2343 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-24 21:36:40.960  2343  2343 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
10-24 21:36:40.982   508   522 D CoreBackPreview: Window{20063c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@eb6bd1a, mPriority=0, mIsAnimationCallback=false}
10-24 21:36:41.083   508   525 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +603ms
10-24 21:36:41.084   799   832 V WindowManagerShell: onTransitionReady android.os.BinderProxy@7f100da: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity)/@0xb7bda01 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity)/@0xdee50a6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:36:41.084   799   832 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity)/@0xb7bda01 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity)/@0xdee50a6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:36:41.084   799   832 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity)/@0xb7bda01 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity)/@0xdee50a6 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:36:41.085   508   525 V WindowManager: Sent Transition #7 createdAt=10-24 21:36:40.480 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=95408 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c27f568 Task{2e65308 #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{c78e0d4 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 21:36:41.085   508   525 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b10cc09 u0 com.ghprotocol.app/.MainActivity)/@0x2f390e6 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{56c0ab u0 com.ghprotocol.app/.MainActivity)/@0x6c8f341 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 21:36:41.279   508  1131 I ImeTracker: com.ghprotocol.app:495ca2f7: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-24 21:36:41.279   508  1131 I ImeTracker: com.ghprotocol.app:495ca2f7: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-24 21:36:48.772  2425  2425 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:36:48.774  2425  2425 I AndroidRuntime: Using default boot image
10-24 21:36:48.774  2425  2425 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:36:48.841  2425  2425 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:36:49.940  2425  2425 D AndroidRuntime: Shutting down VM
10-24 21:37:02.977  2451  2451 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:37:02.980  2451  2451 I AndroidRuntime: Using default boot image
10-24 21:37:02.980  2451  2451 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:37:03.041  2451  2451 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:37:04.097  2451  2451 D AndroidRuntime: Shutting down VM
10-24 21:37:17.105  2476  2476 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:37:17.107  2476  2476 I AndroidRuntime: Using default boot image
10-24 21:37:17.107  2476  2476 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:37:17.170  2476  2476 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:37:18.211  2476  2476 D AndroidRuntime: Shutting down VM
10-24 21:37:31.239  2501  2501 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:37:31.241  2501  2501 I AndroidRuntime: Using default boot image
10-24 21:37:31.241  2501  2501 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:37:31.301  2501  2501 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:37:32.347  2501  2501 D AndroidRuntime: Shutting down VM
10-24 21:37:45.334  2526  2526 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:37:45.336  2526  2526 I AndroidRuntime: Using default boot image
10-24 21:37:45.337  2526  2526 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:37:45.397  2526  2526 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:37:46.441  2526  2526 D AndroidRuntime: Shutting down VM
10-24 21:37:59.472  2549  2549 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:37:59.475  2549  2549 I AndroidRuntime: Using default boot image
10-24 21:37:59.475  2549  2549 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:37:59.535  2549  2549 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:38:00.571  2549  2549 D AndroidRuntime: Shutting down VM
10-24 21:38:13.603  2574  2574 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:38:13.606  2574  2574 I AndroidRuntime: Using default boot image
10-24 21:38:13.606  2574  2574 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:38:13.670  2574  2574 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:38:14.711  2574  2574 D AndroidRuntime: Shutting down VM
10-24 21:38:27.708  2597  2597 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:38:27.710  2597  2597 I AndroidRuntime: Using default boot image
10-24 21:38:27.710  2597  2597 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:38:27.771  2597  2597 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:38:28.810  2597  2597 D AndroidRuntime: Shutting down VM
10-24 21:38:41.857  2622  2622 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:38:41.859  2622  2622 I AndroidRuntime: Using default boot image
10-24 21:38:41.859  2622  2622 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:38:41.922  2622  2622 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:38:42.964  2622  2622 D AndroidRuntime: Shutting down VM
10-24 21:38:55.981  2647  2647 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:38:55.983  2647  2647 I AndroidRuntime: Using default boot image
10-24 21:38:55.983  2647  2647 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:38:56.051  2647  2647 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:38:57.088  2647  2647 D AndroidRuntime: Shutting down VM
10-24 21:39:10.070  2670  2670 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:39:10.072  2670  2670 I AndroidRuntime: Using default boot image
10-24 21:39:10.072  2670  2670 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:39:10.133  2670  2670 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:39:11.169  2670  2670 D AndroidRuntime: Shutting down VM
10-24 21:39:24.206  2695  2695 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:39:24.209  2695  2695 I AndroidRuntime: Using default boot image
10-24 21:39:24.209  2695  2695 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:39:24.271  2695  2695 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:39:25.311  2695  2695 D AndroidRuntime: Shutting down VM
10-24 21:39:38.295  2718  2718 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:39:38.298  2718  2718 I AndroidRuntime: Using default boot image
10-24 21:39:38.298  2718  2718 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:39:38.358  2718  2718 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:39:39.390  2718  2718 D AndroidRuntime: Shutting down VM
10-24 21:39:52.403  2743  2743 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:39:52.405  2743  2743 I AndroidRuntime: Using default boot image
10-24 21:39:52.405  2743  2743 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:39:52.467  2743  2743 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:39:53.507  2743  2743 D AndroidRuntime: Shutting down VM
10-24 21:40:06.551  2767  2767 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:40:06.554  2767  2767 I AndroidRuntime: Using default boot image
10-24 21:40:06.554  2767  2767 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:40:06.618  2767  2767 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:40:07.656  2767  2767 D AndroidRuntime: Shutting down VM
10-24 21:40:20.655  2790  2790 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:40:20.657  2790  2790 I AndroidRuntime: Using default boot image
10-24 21:40:20.657  2790  2790 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:40:20.724  2790  2790 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:40:21.766  2790  2790 D AndroidRuntime: Shutting down VM
10-24 21:40:34.776  2816  2816 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:40:34.778  2816  2816 I AndroidRuntime: Using default boot image
10-24 21:40:34.778  2816  2816 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:40:34.844  2816  2816 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:40:35.876  2816  2816 D AndroidRuntime: Shutting down VM
10-24 21:40:48.875  2839  2839 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:40:48.877  2839  2839 I AndroidRuntime: Using default boot image
10-24 21:40:48.877  2839  2839 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:40:48.947  2839  2839 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:40:49.986  2839  2839 D AndroidRuntime: Shutting down VM
10-24 21:41:02.995  2864  2864 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:41:02.997  2864  2864 I AndroidRuntime: Using default boot image
10-24 21:41:02.997  2864  2864 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:41:03.065  2864  2864 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:41:04.109  2864  2864 D AndroidRuntime: Shutting down VM
10-24 21:41:17.143  2890  2890 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:41:17.146  2890  2890 I AndroidRuntime: Using default boot image
10-24 21:41:17.146  2890  2890 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:41:17.214  2890  2890 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:41:18.255  2890  2890 D AndroidRuntime: Shutting down VM
10-24 21:41:31.242  2913  2913 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:41:31.244  2913  2913 I AndroidRuntime: Using default boot image
10-24 21:41:31.244  2913  2913 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:41:31.309  2913  2913 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:41:32.346  2913  2913 D AndroidRuntime: Shutting down VM
10-24 21:41:45.365  2938  2938 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:41:45.368  2938  2938 I AndroidRuntime: Using default boot image
10-24 21:41:45.368  2938  2938 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:41:45.431  2938  2938 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:41:46.476  2938  2938 D AndroidRuntime: Shutting down VM
10-24 21:41:59.466  2961  2961 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:41:59.469  2961  2961 I AndroidRuntime: Using default boot image
10-24 21:41:59.469  2961  2961 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:41:59.533  2961  2961 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:42:00.579  2961  2961 D AndroidRuntime: Shutting down VM
10-24 21:42:13.584  2986  2986 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:42:13.587  2986  2986 I AndroidRuntime: Using default boot image
10-24 21:42:13.587  2986  2986 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:42:13.655  2986  2986 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:42:14.687  2986  2986 D AndroidRuntime: Shutting down VM
10-24 21:42:27.703  3011  3011 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:42:27.705  3011  3011 I AndroidRuntime: Using default boot image
10-24 21:42:27.705  3011  3011 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:42:27.769  3011  3011 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:42:28.804  3011  3011 D AndroidRuntime: Shutting down VM
10-24 21:42:41.793  3034  3034 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:42:41.796  3034  3034 I AndroidRuntime: Using default boot image
10-24 21:42:41.796  3034  3034 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:42:41.861  3034  3034 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:42:42.898  3034  3034 D AndroidRuntime: Shutting down VM
10-24 21:42:55.921  3059  3059 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:42:55.923  3059  3059 I AndroidRuntime: Using default boot image
10-24 21:42:55.923  3059  3059 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:42:55.986  3059  3059 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:42:57.018  3059  3059 D AndroidRuntime: Shutting down VM
10-24 21:43:10.007  3082  3082 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:43:10.009  3082  3082 I AndroidRuntime: Using default boot image
10-24 21:43:10.009  3082  3082 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:43:10.078  3082  3082 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:43:11.124  3082  3082 D AndroidRuntime: Shutting down VM
10-24 21:43:24.141  3109  3109 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:43:24.143  3109  3109 I AndroidRuntime: Using default boot image
10-24 21:43:24.143  3109  3109 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:43:24.216  3109  3109 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:43:25.248  3109  3109 D AndroidRuntime: Shutting down VM
10-24 21:43:38.255  3134  3134 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 21:43:38.257  3134  3134 I AndroidRuntime: Using default boot image
10-24 21:43:38.257  3134  3134 I AndroidRuntime: Leaving lock profiling enabled
10-24 21:43:38.322  3134  3134 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 21:43:39.354  3134  3134 D AndroidRuntime: Shutting down VM


