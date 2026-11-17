## gh-protocol E2E log — 2026-11-17T14:07:51Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-11-17T13:56:40Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Nov 17 13:53 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Nov 17 13:57 .
drwxr-xr-x 3 runner runner 4096 Nov 17 13:57 ..
drwxr-xr-x 3 runner runner 4096 Nov 17 13:57 gh_test.avd
-rw-r--r-- 1 runner runner  115 Nov 17 13:57 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.13.0 (build_id 16740729) (CL:N/A)
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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15983 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15983 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 3010
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
INFO         |   androidboot.serialno=EMULATOR37X2X13X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x761eb1a01000 as it is in the protected range from 0x761db1a00000 to 0x761eb1c00000
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
INFO         | Boot completed in 28827 ms
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
> Task :app:packageDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugShaders
> Task :app:desugarDebugFileDependencies
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeLibDexDebug
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
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:608:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1794923674002.json

BUILD SUCCESSFUL in 2m 14s
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
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~8s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3318)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       3318   335   13950184 183976 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp      130      0 10.0.2.16:44048         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43976         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:44044         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:44042         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:44040         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:44024         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:47116         142.251.157.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:49582         172.217.115.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:44008         172.217.117.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:42784         172.217.113.4:443       CLOSE_WAIT 
tcp        0      0 10.0.2.16:45118         142.251.157.119:443     CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:37763  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:40797  [::]:*                  LISTEN     
tcp6       0      0 ::ffff:10.0.2.16:57650  ::ffff:74.125.137.:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:58640  ::ffff:142.251.218.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:57710  ::ffff:142.251.214.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:50734  ::ffff:172.217.118.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:46868  ::ffff:142.251.156.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:50744  ::ffff:172.217.118.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:45562  ::ffff:104.154.125.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{e06bdb1 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{e51d46 3318:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~HC2R838sa3CulBQCEhUP6w==/com.ghprotocol.app-qHumodi3J291cfvOn-OPFA==/base.apk
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
      windows=[Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-9m3s972ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{e06bdb1 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{e51d46 3318:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~HC2R838sa3CulBQCEhUP6w==/com.ghprotocol.app-qHumodi3J291cfvOn-OPFA==/base.apk
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
      windows=[Window{57f7e67 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-9m9s732ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@119971744
  deepestLastOrientationSource=ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=87
  mCurrentFocus=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{e06bdb1 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{1f9cf1e #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{a17b5d2 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{829f107 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{418d474 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{b410212 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{2bf6761 u0 StatusBar}
    mFocusedWindow=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{404eb72 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
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
      Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {83210000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=cf2e7d4 InputMethod)/@0xf1ab472 - animation-leash of insets_animation)/@0x17c3e28 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{cf2e7d4 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=cf2e7d4 InputMethod)/@0xf1ab472 - animation-leash of insets_animation)/@0x17c3e28
        mControlTarget=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false
      InsetsSourceProvider
        mSource=InsetsSource id=83210006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{2bf6761 u0 StatusBar}
      InsetsSourceProvider
        mSource=InsetsSource id=83210005 type=mandatorySystemGestures frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
--
        mWindowContainer=Window{2bf6761 u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=2bf6761 StatusBar)/@0x3aa189d - animation-leash of insets_animation)/@0x7c6d741
        mControlTarget=Window{e9616e u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false

--
        (multi-window) Task{505fd9d #3 type=undefined}
        (multi-window) Task{b410212 #4 type=undefined}
        (fullscreen) Task{e90e296 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{e51d46 3318:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray (geo data):
total 6212
drwx------ 2 u0_a192 u0_a192    4096 2026-11-17 13:58 .
drwxrwx--x 3 u0_a192 u0_a192    4096 2026-11-17 13:58 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-11-17 13:58 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-11-17 13:58 geosite.dat
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
runtime config (first 1400 bytes):
core exit line:
GhDiag (connect-flow trace):
--------- beginning of main
11-17 13:58:44.500  3318  3318 D GhDiag  : connect: tap -> CHECKING (have sub=true)
11-17 13:58:44.500  3318  3318 D GhDiag  : connect: sub ok entries=3 -> PREPARING (core extract+version)
11-17 13:58:44.765  3318  3318 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
11-17 13:58:44.765  3318  3318 D GhDiag  : connect: FAILED — core unavailable/old (min=26.11.21)
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
d 2000 <<<<<<
11-17 14:01:06.479  6467  6467 I AndroidRuntime: Using default boot image
11-17 14:01:06.479  6467  6467 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:06.536  6467  6467 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:07.572  6467  6467 D AndroidRuntime: Shutting down VM
11-17 14:01:12.494  6495  6495 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:12.497  6495  6495 I AndroidRuntime: Using default boot image
11-17 14:01:12.497  6495  6495 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:12.561  6495  6495 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:13.601  6495  6495 D AndroidRuntime: Shutting down VM
11-17 14:01:18.527  6526  6526 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:18.530  6526  6526 I AndroidRuntime: Using default boot image
11-17 14:01:18.530  6526  6526 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:18.587  6526  6526 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:19.625  6526  6526 D AndroidRuntime: Shutting down VM
11-17 14:01:24.545  6549  6549 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:24.548  6549  6549 I AndroidRuntime: Using default boot image
11-17 14:01:24.548  6549  6549 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:24.607  6549  6549 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:25.657  6549  6549 D AndroidRuntime: Shutting down VM
11-17 14:01:30.573  6578  6578 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:30.575  6578  6578 I AndroidRuntime: Using default boot image
11-17 14:01:30.575  6578  6578 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:30.632  6578  6578 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:31.665  6578  6578 D AndroidRuntime: Shutting down VM
11-17 14:01:36.575  6601  6601 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:36.577  6601  6601 I AndroidRuntime: Using default boot image
11-17 14:01:36.577  6601  6601 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:36.634  6601  6601 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:37.672  6601  6601 D AndroidRuntime: Shutting down VM
11-17 14:01:42.584  6626  6626 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:42.587  6626  6626 I AndroidRuntime: Using default boot image
11-17 14:01:42.587  6626  6626 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:42.647  6626  6626 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:43.679  6626  6626 D AndroidRuntime: Shutting down VM
11-17 14:01:48.606  6651  6651 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:48.609  6651  6651 I AndroidRuntime: Using default boot image
11-17 14:01:48.609  6651  6651 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:48.666  6651  6651 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:49.693  6651  6651 D AndroidRuntime: Shutting down VM
11-17 14:01:54.600  6676  6676 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:01:54.602  6676  6676 I AndroidRuntime: Using default boot image
11-17 14:01:54.602  6676  6676 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:01:54.663  6676  6676 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:01:55.697  6676  6676 D AndroidRuntime: Shutting down VM
11-17 14:02:00.603  6700  6700 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:00.606  6700  6700 I AndroidRuntime: Using default boot image
11-17 14:02:00.606  6700  6700 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:00.662  6700  6700 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:01.690  6700  6700 D AndroidRuntime: Shutting down VM
11-17 14:02:06.597  6725  6725 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:06.600  6725  6725 I AndroidRuntime: Using default boot image
11-17 14:02:06.600  6725  6725 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:06.656  6725  6725 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:07.700  6725  6725 D AndroidRuntime: Shutting down VM
11-17 14:02:12.609  6756  6756 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:12.612  6756  6756 I AndroidRuntime: Using default boot image
11-17 14:02:12.612  6756  6756 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:12.671  6756  6756 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:13.710  6756  6756 D AndroidRuntime: Shutting down VM
11-17 14:02:18.636  6782  6782 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:18.639  6782  6782 I AndroidRuntime: Using default boot image
11-17 14:02:18.639  6782  6782 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:18.699  6782  6782 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:19.735  6782  6782 D AndroidRuntime: Shutting down VM
11-17 14:02:24.648  6806  6806 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:24.651  6806  6806 I AndroidRuntime: Using default boot image
11-17 14:02:24.651  6806  6806 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:24.712  6806  6806 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:25.746  6806  6806 D AndroidRuntime: Shutting down VM
11-17 14:02:30.685  6829  6829 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:30.687  6829  6829 I AndroidRuntime: Using default boot image
11-17 14:02:30.687  6829  6829 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:30.746  6829  6829 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:31.779  6829  6829 D AndroidRuntime: Shutting down VM
11-17 14:02:36.688  6852  6852 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:36.690  6852  6852 I AndroidRuntime: Using default boot image
11-17 14:02:36.690  6852  6852 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:36.749  6852  6852 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:37.785  6852  6852 D AndroidRuntime: Shutting down VM
11-17 14:02:42.698  6875  6875 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:42.700  6875  6875 I AndroidRuntime: Using default boot image
11-17 14:02:42.700  6875  6875 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:42.758  6875  6875 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:43.802  6875  6875 D AndroidRuntime: Shutting down VM
11-17 14:02:48.728  6900  6900 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:48.731  6900  6900 I AndroidRuntime: Using default boot image
11-17 14:02:48.731  6900  6900 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:48.790  6900  6900 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:49.829  6900  6900 D AndroidRuntime: Shutting down VM
11-17 14:02:54.748  6937  6937 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:02:54.750  6937  6937 I AndroidRuntime: Using default boot image
11-17 14:02:54.750  6937  6937 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:02:54.808  6937  6937 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:02:55.852  6937  6937 D AndroidRuntime: Shutting down VM
11-17 14:03:00.761  6960  6960 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:00.763  6960  6960 I AndroidRuntime: Using default boot image
11-17 14:03:00.763  6960  6960 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:00.819  6960  6960 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:01.850  6960  6960 D AndroidRuntime: Shutting down VM
11-17 14:03:06.749  6985  6985 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:06.751  6985  6985 I AndroidRuntime: Using default boot image
11-17 14:03:06.751  6985  6985 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:06.804  6985  6985 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:07.849  6985  6985 D AndroidRuntime: Shutting down VM
11-17 14:03:12.756  7008  7008 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:12.759  7008  7008 I AndroidRuntime: Using default boot image
11-17 14:03:12.759  7008  7008 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:12.812  7008  7008 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:13.852  7008  7008 D AndroidRuntime: Shutting down VM
11-17 14:03:18.770  7037  7037 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:18.772  7037  7037 I AndroidRuntime: Using default boot image
11-17 14:03:18.772  7037  7037 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:18.827  7037  7037 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:19.874  7037  7037 D AndroidRuntime: Shutting down VM
11-17 14:03:24.797  7062  7062 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:24.799  7062  7062 I AndroidRuntime: Using default boot image
11-17 14:03:24.799  7062  7062 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:24.861  7062  7062 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:25.896  7062  7062 D AndroidRuntime: Shutting down VM
11-17 14:03:30.810  7090  7090 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:30.812  7090  7090 I AndroidRuntime: Using default boot image
11-17 14:03:30.812  7090  7090 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:30.866  7090  7090 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:31.897  7090  7090 D AndroidRuntime: Shutting down VM
11-17 14:03:36.805  7143  7143 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:36.808  7143  7143 I AndroidRuntime: Using default boot image
11-17 14:03:36.808  7143  7143 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:36.863  7143  7143 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:37.892  7143  7143 D AndroidRuntime: Shutting down VM
11-17 14:03:42.804  7167  7167 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:42.806  7167  7167 I AndroidRuntime: Using default boot image
11-17 14:03:42.806  7167  7167 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:42.864  7167  7167 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:43.897  7167  7167 D AndroidRuntime: Shutting down VM
11-17 14:03:48.814  7193  7193 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:48.817  7193  7193 I AndroidRuntime: Using default boot image
11-17 14:03:48.817  7193  7193 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:48.874  7193  7193 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:49.930  7193  7193 D AndroidRuntime: Shutting down VM
11-17 14:03:54.846  7217  7217 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:03:54.849  7217  7217 I AndroidRuntime: Using default boot image
11-17 14:03:54.849  7217  7217 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:03:54.909  7217  7217 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:03:55.950  7217  7217 D AndroidRuntime: Shutting down VM
11-17 14:04:00.854  7241  7241 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:00.857  7241  7241 I AndroidRuntime: Using default boot image
11-17 14:04:00.857  7241  7241 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:00.917  7241  7241 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:01.948  7241  7241 D AndroidRuntime: Shutting down VM
11-17 14:04:06.863  7266  7266 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:06.866  7266  7266 I AndroidRuntime: Using default boot image
11-17 14:04:06.866  7266  7266 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:06.922  7266  7266 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:07.958  7266  7266 D AndroidRuntime: Shutting down VM
11-17 14:04:12.863  7291  7291 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:12.866  7291  7291 I AndroidRuntime: Using default boot image
11-17 14:04:12.866  7291  7291 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:12.923  7291  7291 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:13.968  7291  7291 D AndroidRuntime: Shutting down VM
11-17 14:04:18.895  7317  7317 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:18.898  7317  7317 I AndroidRuntime: Using default boot image
11-17 14:04:18.898  7317  7317 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:18.958  7317  7317 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:19.998  7317  7317 D AndroidRuntime: Shutting down VM
11-17 14:04:24.928  7341  7341 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:24.930  7341  7341 I AndroidRuntime: Using default boot image
11-17 14:04:24.930  7341  7341 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:24.987  7341  7341 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:26.017  7341  7341 D AndroidRuntime: Shutting down VM
11-17 14:04:30.949   522   572 I AppsFilter: interaction: PackageSetting{f9fdf9b com.ghprotocol.app/10192} -> PackageSetting{42436b4 com.google.android.contacts/10155} BLOCKED
11-17 14:04:30.973  7470  7470 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:30.976  7470  7470 I AndroidRuntime: Using default boot image
11-17 14:04:30.976  7470  7470 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:31.036  7470  7470 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:32.058  7470  7470 D AndroidRuntime: Shutting down VM
11-17 14:04:36.962  7496  7496 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:36.964  7496  7496 I AndroidRuntime: Using default boot image
11-17 14:04:36.964  7496  7496 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:37.019  7496  7496 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:38.042  7496  7496 D AndroidRuntime: Shutting down VM
11-17 14:04:40.983   522   572 I AppsFilter: interaction: PackageSetting{f9fdf9b com.ghprotocol.app/10192} -> PackageSetting{87b7020 com.google.android.contacts/10155} BLOCKED
11-17 14:04:42.954  7536  7536 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:42.956  7536  7536 I AndroidRuntime: Using default boot image
11-17 14:04:42.956  7536  7536 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:43.017  7536  7536 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:44.050  7536  7536 D AndroidRuntime: Shutting down VM
11-17 14:04:48.976  7561  7561 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:48.978  7561  7561 I AndroidRuntime: Using default boot image
11-17 14:04:48.978  7561  7561 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:49.034  7561  7561 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:50.076  7561  7561 D AndroidRuntime: Shutting down VM
11-17 14:04:54.991  7584  7584 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:04:54.994  7584  7584 I AndroidRuntime: Using default boot image
11-17 14:04:54.994  7584  7584 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:04:55.054  7584  7584 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:04:56.085  7584  7584 D AndroidRuntime: Shutting down VM
11-17 14:05:00.989  7607  7607 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:00.991  7607  7607 I AndroidRuntime: Using default boot image
11-17 14:05:00.991  7607  7607 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:01.051  7607  7607 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:02.086  7607  7607 D AndroidRuntime: Shutting down VM
11-17 14:05:06.992  7631  7631 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:06.995  7631  7631 I AndroidRuntime: Using default boot image
11-17 14:05:06.995  7631  7631 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:07.053  7631  7631 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:08.080  7631  7631 D AndroidRuntime: Shutting down VM
11-17 14:05:12.987  7654  7654 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:12.990  7654  7654 I AndroidRuntime: Using default boot image
11-17 14:05:12.990  7654  7654 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:13.063  7654  7654 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:14.100  7654  7654 D AndroidRuntime: Shutting down VM
11-17 14:05:19.017  7679  7679 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:19.020  7679  7679 I AndroidRuntime: Using default boot image
11-17 14:05:19.020  7679  7679 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:19.076  7679  7679 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:20.117  7679  7679 D AndroidRuntime: Shutting down VM
11-17 14:05:25.023  7702  7702 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:25.025  7702  7702 I AndroidRuntime: Using default boot image
11-17 14:05:25.025  7702  7702 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:25.085  7702  7702 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:26.122  7702  7702 D AndroidRuntime: Shutting down VM
11-17 14:05:31.023  7725  7725 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:31.025  7725  7725 I AndroidRuntime: Using default boot image
11-17 14:05:31.025  7725  7725 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:31.081  7725  7725 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:32.108  7725  7725 D AndroidRuntime: Shutting down VM
11-17 14:05:37.046  7748  7748 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:37.048  7748  7748 I AndroidRuntime: Using default boot image
11-17 14:05:37.048  7748  7748 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:37.105  7748  7748 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:38.140  7748  7748 D AndroidRuntime: Shutting down VM
11-17 14:05:43.044  7772  7772 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:43.046  7772  7772 I AndroidRuntime: Using default boot image
11-17 14:05:43.046  7772  7772 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:43.105  7772  7772 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:44.162  7772  7772 D AndroidRuntime: Shutting down VM
11-17 14:05:49.102  7798  7798 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:49.104  7798  7798 I AndroidRuntime: Using default boot image
11-17 14:05:49.104  7798  7798 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:49.161  7798  7798 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:50.196  7798  7798 D AndroidRuntime: Shutting down VM
11-17 14:05:55.102  7821  7821 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:05:55.104  7821  7821 I AndroidRuntime: Using default boot image
11-17 14:05:55.104  7821  7821 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:05:55.160  7821  7821 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:05:56.196  7821  7821 D AndroidRuntime: Shutting down VM
11-17 14:06:01.105  7844  7844 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:01.107  7844  7844 I AndroidRuntime: Using default boot image
11-17 14:06:01.107  7844  7844 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:01.162  7844  7844 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:02.197  7844  7844 D AndroidRuntime: Shutting down VM
11-17 14:06:07.134  7867  7867 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:07.136  7867  7867 I AndroidRuntime: Using default boot image
11-17 14:06:07.136  7867  7867 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:07.194  7867  7867 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:08.234  7867  7867 D AndroidRuntime: Shutting down VM
11-17 14:06:13.136  7892  7892 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:13.139  7892  7892 I AndroidRuntime: Using default boot image
11-17 14:06:13.139  7892  7892 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:13.198  7892  7892 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:14.230  7892  7892 D AndroidRuntime: Shutting down VM
11-17 14:06:19.158  7917  7917 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:19.161  7917  7917 I AndroidRuntime: Using default boot image
11-17 14:06:19.161  7917  7917 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:19.219  7917  7917 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:20.253  7917  7917 D AndroidRuntime: Shutting down VM
11-17 14:06:25.164  7940  7940 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:25.167  7940  7940 I AndroidRuntime: Using default boot image
11-17 14:06:25.167  7940  7940 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:25.224  7940  7940 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:26.259  7940  7940 D AndroidRuntime: Shutting down VM
11-17 14:06:31.176  7973  7973 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:31.178  7973  7973 I AndroidRuntime: Using default boot image
11-17 14:06:31.178  7973  7973 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:31.238  7973  7973 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:32.272  7973  7973 D AndroidRuntime: Shutting down VM
11-17 14:06:37.178  7997  7997 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:37.180  7997  7997 I AndroidRuntime: Using default boot image
11-17 14:06:37.180  7997  7997 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:37.237  7997  7997 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:38.272  7997  7997 D AndroidRuntime: Shutting down VM
11-17 14:06:43.180  8020  8020 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:43.183  8020  8020 I AndroidRuntime: Using default boot image
11-17 14:06:43.183  8020  8020 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:43.244  8020  8020 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:44.280  8020  8020 D AndroidRuntime: Shutting down VM
11-17 14:06:49.211  8045  8045 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:49.213  8045  8045 I AndroidRuntime: Using default boot image
11-17 14:06:49.213  8045  8045 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:49.274  8045  8045 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:50.315  8045  8045 D AndroidRuntime: Shutting down VM
11-17 14:06:55.224  8068  8068 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:06:55.227  8068  8068 I AndroidRuntime: Using default boot image
11-17 14:06:55.227  8068  8068 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:06:55.288  8068  8068 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:06:56.326  8068  8068 D AndroidRuntime: Shutting down VM
11-17 14:07:01.234  8094  8094 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:01.237  8094  8094 I AndroidRuntime: Using default boot image
11-17 14:07:01.237  8094  8094 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:01.295  8094  8094 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:02.327  8094  8094 D AndroidRuntime: Shutting down VM
11-17 14:07:07.245  8117  8117 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:07.248  8117  8117 I AndroidRuntime: Using default boot image
11-17 14:07:07.248  8117  8117 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:07.307  8117  8117 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:08.342  8117  8117 D AndroidRuntime: Shutting down VM
11-17 14:07:13.263  8140  8140 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:13.265  8140  8140 I AndroidRuntime: Using default boot image
11-17 14:07:13.265  8140  8140 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:13.324  8140  8140 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:14.362  8140  8140 D AndroidRuntime: Shutting down VM
11-17 14:07:19.283  8172  8172 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:19.286  8172  8172 I AndroidRuntime: Using default boot image
11-17 14:07:19.286  8172  8172 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:19.346  8172  8172 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:20.381  8172  8172 D AndroidRuntime: Shutting down VM
11-17 14:07:25.326  8209  8209 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:25.329  8209  8209 I AndroidRuntime: Using default boot image
11-17 14:07:25.329  8209  8209 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:25.392  8209  8209 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:26.433  8209  8209 D AndroidRuntime: Shutting down VM
11-17 14:07:31.337  8233  8233 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:31.340  8233  8233 I AndroidRuntime: Using default boot image
11-17 14:07:31.340  8233  8233 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:31.401  8233  8233 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:32.432  8233  8233 D AndroidRuntime: Shutting down VM
11-17 14:07:37.343  8256  8256 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:37.346  8256  8256 I AndroidRuntime: Using default boot image
11-17 14:07:37.346  8256  8256 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:37.401  8256  8256 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:38.435  8256  8256 D AndroidRuntime: Shutting down VM
11-17 14:07:43.340  8279  8279 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:07:43.342  8279  8279 I AndroidRuntime: Using default boot image
11-17 14:07:43.342  8279  8279 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:07:43.402  8279  8279 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:07:44.440  8279  8279 D AndroidRuntime: Shutting down VM


