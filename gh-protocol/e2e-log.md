## gh-protocol E2E log — 2026-11-17T14:22:03Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-11-17T14:11:19Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Nov 17 14:07 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Nov 17 14:11 .
drwxr-xr-x 3 runner runner 4096 Nov 17 14:11 ..
drwxr-xr-x 3 runner runner 4096 Nov 17 14:11 gh_test.avd
-rw-r--r-- 1 runner runner  115 Nov 17 14:11 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 3325
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
WARNING: cannnot unmap ptr 0x7083b5c01000 as it is in the protected range from 0x7082b5c00000 to 0x7083b5e00000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Successfully initialized netsim WiFi
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
INFO         | Boot completed in 40097 ms
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
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:checkDebugAarMetadata
> Task :app:mapDebugSourceSetPaths
> Task :app:mergeDebugShaders
> Task :app:javaPreCompileDebug
> Task :app:desugarDebugFileDependencies
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:compressDebugAssets
> Task :app:mergeDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:processDebugResources
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1794924504798.json

BUILD SUCCESSFUL in 2m 47s
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
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3142)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       3142   337   13876600 185012 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp      130      0 10.0.2.16:44764         142.251.153.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55348         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55332         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55318         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:54470         172.217.115.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55304         172.217.113.4:443       CLOSE_WAIT 
tcp        0      0 10.0.2.16:42650         142.251.151.119:443     CLOSE_WAIT 
tcp      130      0 10.0.2.16:51628         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:51400         172.217.118.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55326         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55356         172.217.113.4:443       CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:46517  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:43689  [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:45136  ::ffff:142.251.154.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:58272  ::ffff:172.217.112.:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.16:54242  ::ffff:172.253.133:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:56104  ::ffff:104.154.125.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:58280  ::ffff:172.217.112.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:48956  ::ffff:173.194.46.1:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:58528  ::ffff:142.250.123.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{de8acd0 u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{b9a7dd8 3142:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~57QEsxbm9yTolNRVi_cqiA==/com.ghprotocol.app-rwIU7OsRe_uJ57Z-JezcQw==/base.apk
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
      windows=[Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-9m15s45ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{de8acd0 u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{b9a7dd8 3142:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~57QEsxbm9yTolNRVi_cqiA==/com.ghprotocol.app-rwIU7OsRe_uJ57Z-JezcQw==/base.apk
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
      windows=[Window{fb97f2 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-9m21s131ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@237319761
  deepestLastOrientationSource=ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=91
  mCurrentFocus=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{de8acd0 u0 com.ghprotocol.app/.MainActivity t8}
      * Task{50e17b7 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{668b4ab #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{b32e6fa u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{7ce13c5 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{bf0b44b #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{e5f88af u0 StatusBar}
    mFocusedWindow=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{25349d5 u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=7a600006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {7a600000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=7a600006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{e5f88af u0 StatusBar}
--
        mWindowContainer=Window{e5f88af u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=e5f88af StatusBar)/@0xf09fb9f - animation-leash of insets_animation)/@0xabbb577
        mControlTarget=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=6b05bd7 InputMethod)/@0x57f17ad - animation-leash of insets_animation)/@0x440b5e4 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{6b05bd7 u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=6b05bd7 InputMethod)/@0x57f17ad - animation-leash of insets_animation)/@0x440b5e4
        mControlTarget=Window{f16cf8f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{c22a11a #3 type=undefined}
        (multi-window) Task{bf0b44b #4 type=undefined}
        (fullscreen) Task{9c98ce2 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{b9a7dd8 3142:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10167:1]
app filesDir/xray (geo data):
total 6212
drwx------ 2 u0_a192 u0_a192    4096 2026-11-17 14:12 .
drwxrwx--x 3 u0_a192 u0_a192    4096 2026-11-17 14:12 ..
-rw------- 1 u0_a192 u0_a192 3977011 2026-11-17 14:12 geoip.dat
-rw------- 1 u0_a192 u0_a192 2358471 2026-11-17 14:12 geosite.dat
nativeLibraryDir (bundled core must be here, exec_allowed):
xray-err.log:
xray-out.log (Xray writes its logs to stdout):
runtime config (first 1400 bytes):
core exit line:
GhDiag (connect-flow trace):
=== E2E FAILED: tunnel not up (xray/:10808) — xray process not running and :10808 not listening (core exited — see xray-out/err logs) ===


### e2e-logcat.log (crashes + app + vpn, tail)
7 14:15:07.438  6309  6309 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:07.518  6309  6309 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:08.600  6309  6309 D AndroidRuntime: Shutting down VM
11-17 14:15:13.588  6334  6334 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:13.591  6334  6334 I AndroidRuntime: Using default boot image
11-17 14:15:13.591  6334  6334 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:13.672  6334  6334 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:14.741  6334  6334 D AndroidRuntime: Shutting down VM
11-17 14:15:19.699  6358  6358 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:19.703  6358  6358 I AndroidRuntime: Using default boot image
11-17 14:15:19.703  6358  6358 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:19.781  6358  6358 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:20.864  6358  6358 D AndroidRuntime: Shutting down VM
11-17 14:15:25.837  6383  6383 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:25.841  6383  6383 I AndroidRuntime: Using default boot image
11-17 14:15:25.841  6383  6383 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:25.922  6383  6383 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:27.030  6383  6383 D AndroidRuntime: Shutting down VM
11-17 14:15:31.992  6411  6411 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:31.996  6411  6411 I AndroidRuntime: Using default boot image
11-17 14:15:31.996  6411  6411 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:32.074  6411  6411 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:33.162  6411  6411 D AndroidRuntime: Shutting down VM
11-17 14:15:38.117  6449  6449 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:38.121  6449  6449 I AndroidRuntime: Using default boot image
11-17 14:15:38.121  6449  6449 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:38.209  6449  6449 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:39.286  6449  6449 D AndroidRuntime: Shutting down VM
11-17 14:15:44.247  6473  6473 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:44.250  6473  6473 I AndroidRuntime: Using default boot image
11-17 14:15:44.250  6473  6473 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:44.336  6473  6473 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:45.405  6473  6473 D AndroidRuntime: Shutting down VM
11-17 14:15:50.347  6496  6496 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:50.350  6496  6496 I AndroidRuntime: Using default boot image
11-17 14:15:50.350  6496  6496 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:50.427  6496  6496 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:51.502  6496  6496 D AndroidRuntime: Shutting down VM
11-17 14:15:56.460  6522  6522 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:15:56.464  6522  6522 I AndroidRuntime: Using default boot image
11-17 14:15:56.464  6522  6522 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:15:56.542  6522  6522 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:15:57.596  6522  6522 D AndroidRuntime: Shutting down VM
11-17 14:16:02.535  6553  6553 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:02.538  6553  6553 I AndroidRuntime: Using default boot image
11-17 14:16:02.538  6553  6553 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:02.615  6553  6553 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:03.677  6553  6553 D AndroidRuntime: Shutting down VM
11-17 14:16:08.617  6578  6578 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:08.621  6578  6578 I AndroidRuntime: Using default boot image
11-17 14:16:08.621  6578  6578 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:08.697  6578  6578 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:09.764  6578  6578 D AndroidRuntime: Shutting down VM
11-17 14:16:14.746  6602  6602 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:14.749  6602  6602 I AndroidRuntime: Using default boot image
11-17 14:16:14.749  6602  6602 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:14.825  6602  6602 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:15.890  6602  6602 D AndroidRuntime: Shutting down VM
11-17 14:16:20.848  6626  6626 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:20.852  6626  6626 I AndroidRuntime: Using default boot image
11-17 14:16:20.852  6626  6626 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:20.931  6626  6626 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:22.001  6626  6626 D AndroidRuntime: Shutting down VM
11-17 14:16:27.000  6652  6652 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:27.004  6652  6652 I AndroidRuntime: Using default boot image
11-17 14:16:27.004  6652  6652 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:27.084  6652  6652 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:28.140  6652  6652 D AndroidRuntime: Shutting down VM
11-17 14:16:33.082  6675  6675 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:33.085  6675  6675 I AndroidRuntime: Using default boot image
11-17 14:16:33.085  6675  6675 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:33.160  6675  6675 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:34.227  6675  6675 D AndroidRuntime: Shutting down VM
11-17 14:16:39.164  6698  6698 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:39.167  6698  6698 I AndroidRuntime: Using default boot image
11-17 14:16:39.167  6698  6698 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:39.242  6698  6698 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:40.346  6698  6698 D AndroidRuntime: Shutting down VM
11-17 14:16:45.288  6726  6726 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:45.292  6726  6726 I AndroidRuntime: Using default boot image
11-17 14:16:45.292  6726  6726 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:45.367  6726  6726 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:46.443  6726  6726 D AndroidRuntime: Shutting down VM
11-17 14:16:51.411  6751  6751 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:51.414  6751  6751 I AndroidRuntime: Using default boot image
11-17 14:16:51.414  6751  6751 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:51.489  6751  6751 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:52.552  6751  6751 D AndroidRuntime: Shutting down VM
11-17 14:16:57.527  6776  6776 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:16:57.530  6776  6776 I AndroidRuntime: Using default boot image
11-17 14:16:57.530  6776  6776 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:16:57.610  6776  6776 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:16:58.662  6776  6776 D AndroidRuntime: Shutting down VM
11-17 14:17:03.605  6800  6800 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:03.609  6800  6800 I AndroidRuntime: Using default boot image
11-17 14:17:03.609  6800  6800 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:03.684  6800  6800 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:04.735  6800  6800 D AndroidRuntime: Shutting down VM
11-17 14:17:09.693  6824  6824 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:09.696  6824  6824 I AndroidRuntime: Using default boot image
11-17 14:17:09.696  6824  6824 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:09.774  6824  6824 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:10.832  6824  6824 D AndroidRuntime: Shutting down VM
11-17 14:17:15.881  6862  6862 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:15.886  6862  6862 I AndroidRuntime: Using default boot image
11-17 14:17:15.886  6862  6862 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:15.985  6862  6862 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:17.110  6862  6862 D AndroidRuntime: Shutting down VM
11-17 14:17:22.074  6900  6900 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:22.077  6900  6900 I AndroidRuntime: Using default boot image
11-17 14:17:22.077  6900  6900 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:22.157  6900  6900 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:23.237  6900  6900 D AndroidRuntime: Shutting down VM
11-17 14:17:28.193  6930  6930 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:28.196  6930  6930 I AndroidRuntime: Using default boot image
11-17 14:17:28.196  6930  6930 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:28.275  6930  6930 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:29.342  6930  6930 D AndroidRuntime: Shutting down VM
11-17 14:17:34.282  6958  6958 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:34.286  6958  6958 I AndroidRuntime: Using default boot image
11-17 14:17:34.286  6958  6958 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:34.362  6958  6958 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:35.423  6958  6958 D AndroidRuntime: Shutting down VM
11-17 14:17:40.369  6987  6987 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:40.372  6987  6987 I AndroidRuntime: Using default boot image
11-17 14:17:40.372  6987  6987 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:40.450  6987  6987 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:41.512  6987  6987 D AndroidRuntime: Shutting down VM
11-17 14:17:46.450  7010  7010 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:46.453  7010  7010 I AndroidRuntime: Using default boot image
11-17 14:17:46.453  7010  7010 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:46.527  7010  7010 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:47.594  7010  7010 D AndroidRuntime: Shutting down VM
11-17 14:17:52.548  7033  7033 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:52.552  7033  7033 I AndroidRuntime: Using default boot image
11-17 14:17:52.552  7033  7033 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:52.628  7033  7033 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:53.694  7033  7033 D AndroidRuntime: Shutting down VM
11-17 14:17:58.652  7058  7058 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:17:58.655  7058  7058 I AndroidRuntime: Using default boot image
11-17 14:17:58.655  7058  7058 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:17:58.734  7058  7058 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:17:59.787  7058  7058 D AndroidRuntime: Shutting down VM
11-17 14:18:04.731  7081  7081 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:04.735  7081  7081 I AndroidRuntime: Using default boot image
11-17 14:18:04.735  7081  7081 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:04.811  7081  7081 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:05.888  7081  7081 D AndroidRuntime: Shutting down VM
11-17 14:18:10.857  7104  7104 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:10.860  7104  7104 I AndroidRuntime: Using default boot image
11-17 14:18:10.860  7104  7104 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:10.936  7104  7104 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:11.996  7104  7104 D AndroidRuntime: Shutting down VM
11-17 14:18:16.933  7129  7129 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:16.936  7129  7129 I AndroidRuntime: Using default boot image
11-17 14:18:16.936  7129  7129 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:17.012  7129  7129 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:18.066  7129  7129 D AndroidRuntime: Shutting down VM
11-17 14:18:23.019  7153  7153 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:23.023  7153  7153 I AndroidRuntime: Using default boot image
11-17 14:18:23.023  7153  7153 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:23.098  7153  7153 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:24.161  7153  7153 D AndroidRuntime: Shutting down VM
11-17 14:18:29.116  7179  7179 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:29.120  7179  7179 I AndroidRuntime: Using default boot image
11-17 14:18:29.120  7179  7179 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:29.199  7179  7179 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:30.259  7179  7179 D AndroidRuntime: Shutting down VM
11-17 14:18:35.197  7202  7202 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:35.201  7202  7202 I AndroidRuntime: Using default boot image
11-17 14:18:35.201  7202  7202 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:35.277  7202  7202 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:36.342  7202  7202 D AndroidRuntime: Shutting down VM
11-17 14:18:41.282  7228  7228 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:41.285  7228  7228 I AndroidRuntime: Using default boot image
11-17 14:18:41.285  7228  7228 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:41.361  7228  7228 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:42.410  7228  7228 D AndroidRuntime: Shutting down VM
11-17 14:18:47.352  7251  7251 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:47.356  7251  7251 I AndroidRuntime: Using default boot image
11-17 14:18:47.356  7251  7251 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:47.435  7251  7251 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:48.517  7251  7251 D AndroidRuntime: Shutting down VM
11-17 14:18:53.475  7274  7274 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:53.479  7274  7274 I AndroidRuntime: Using default boot image
11-17 14:18:53.479  7274  7274 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:53.556  7274  7274 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:18:54.624  7274  7274 D AndroidRuntime: Shutting down VM
11-17 14:18:59.596  7299  7299 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:18:59.600  7299  7299 I AndroidRuntime: Using default boot image
11-17 14:18:59.600  7299  7299 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:18:59.681  7299  7299 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:00.735  7299  7299 D AndroidRuntime: Shutting down VM
11-17 14:19:05.717  7412  7412 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:05.721  7412  7412 I AndroidRuntime: Using default boot image
11-17 14:19:05.721  7412  7412 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:05.801  7412  7412 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:06.870  7412  7412 D AndroidRuntime: Shutting down VM
11-17 14:19:11.809  7435  7435 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:11.813  7435  7435 I AndroidRuntime: Using default boot image
11-17 14:19:11.813  7435  7435 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:11.888  7435  7435 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:12.944  7435  7435 D AndroidRuntime: Shutting down VM
11-17 14:19:17.894  7464  7464 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:17.898  7464  7464 I AndroidRuntime: Using default boot image
11-17 14:19:17.898  7464  7464 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:17.978  7464  7464 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:19.049  7464  7464 D AndroidRuntime: Shutting down VM
11-17 14:19:23.999  7487  7487 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:24.003  7487  7487 I AndroidRuntime: Using default boot image
11-17 14:19:24.003  7487  7487 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:24.085  7487  7487 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:25.140  7487  7487 D AndroidRuntime: Shutting down VM
11-17 14:19:30.110  7512  7512 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:30.113  7512  7512 I AndroidRuntime: Using default boot image
11-17 14:19:30.113  7512  7512 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:30.190  7512  7512 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:31.239  7512  7512 D AndroidRuntime: Shutting down VM
11-17 14:19:36.191  7535  7535 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:36.194  7535  7535 I AndroidRuntime: Using default boot image
11-17 14:19:36.195  7535  7535 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:36.273  7535  7535 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:37.350  7535  7535 D AndroidRuntime: Shutting down VM
11-17 14:19:42.294  7559  7559 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:42.298  7559  7559 I AndroidRuntime: Using default boot image
11-17 14:19:42.298  7559  7559 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:42.377  7559  7559 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:43.428  7559  7559 D AndroidRuntime: Shutting down VM
11-17 14:19:48.378  7582  7582 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:48.381  7582  7582 I AndroidRuntime: Using default boot image
11-17 14:19:48.381  7582  7582 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:48.458  7582  7582 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:49.538  7582  7582 D AndroidRuntime: Shutting down VM
11-17 14:19:54.476  7610  7610 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:19:54.480  7610  7610 I AndroidRuntime: Using default boot image
11-17 14:19:54.480  7610  7610 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:19:54.554  7610  7610 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:19:55.603  7610  7610 D AndroidRuntime: Shutting down VM
11-17 14:20:00.570  7635  7635 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:00.574  7635  7635 I AndroidRuntime: Using default boot image
11-17 14:20:00.574  7635  7635 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:00.657  7635  7635 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:01.699  7635  7635 D AndroidRuntime: Shutting down VM
11-17 14:20:06.653  7658  7658 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:06.656  7658  7658 I AndroidRuntime: Using default boot image
11-17 14:20:06.656  7658  7658 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:06.737  7658  7658 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:07.784  7658  7658 D AndroidRuntime: Shutting down VM
11-17 14:20:12.758  7682  7682 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:12.761  7682  7682 I AndroidRuntime: Using default boot image
11-17 14:20:12.761  7682  7682 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:12.840  7682  7682 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:13.897  7682  7682 D AndroidRuntime: Shutting down VM
11-17 14:20:18.839  7705  7705 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:18.842  7705  7705 I AndroidRuntime: Using default boot image
11-17 14:20:18.843  7705  7705 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:18.919  7705  7705 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:19.970  7705  7705 D AndroidRuntime: Shutting down VM
11-17 14:20:24.918  7728  7728 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:24.921  7728  7728 I AndroidRuntime: Using default boot image
11-17 14:20:24.921  7728  7728 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:25.004  7728  7728 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:26.069  7728  7728 D AndroidRuntime: Shutting down VM
11-17 14:20:31.047  7753  7753 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:31.051  7753  7753 I AndroidRuntime: Using default boot image
11-17 14:20:31.051  7753  7753 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:31.132  7753  7753 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:32.200  7753  7753 D AndroidRuntime: Shutting down VM
11-17 14:20:37.154  7777  7777 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:37.157  7777  7777 I AndroidRuntime: Using default boot image
11-17 14:20:37.157  7777  7777 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:37.233  7777  7777 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:38.299  7777  7777 D AndroidRuntime: Shutting down VM
11-17 14:20:43.241  7800  7800 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:43.244  7800  7800 I AndroidRuntime: Using default boot image
11-17 14:20:43.244  7800  7800 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:43.322  7800  7800 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:44.409  7800  7800 D AndroidRuntime: Shutting down VM
11-17 14:20:49.362  7824  7824 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:49.365  7824  7824 I AndroidRuntime: Using default boot image
11-17 14:20:49.365  7824  7824 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:49.441  7824  7824 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:50.510  7824  7824 D AndroidRuntime: Shutting down VM
11-17 14:20:55.452  7847  7847 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:20:55.455  7847  7847 I AndroidRuntime: Using default boot image
11-17 14:20:55.455  7847  7847 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:20:55.532  7847  7847 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:20:56.598  7847  7847 D AndroidRuntime: Shutting down VM
11-17 14:21:01.563  7879  7879 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:01.567  7879  7879 I AndroidRuntime: Using default boot image
11-17 14:21:01.567  7879  7879 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:01.643  7879  7879 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:02.725  7879  7879 D AndroidRuntime: Shutting down VM
11-17 14:21:07.676  7908  7908 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:07.680  7908  7908 I AndroidRuntime: Using default boot image
11-17 14:21:07.680  7908  7908 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:07.756  7908  7908 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:08.810  7908  7908 D AndroidRuntime: Shutting down VM
11-17 14:21:13.754  7931  7931 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:13.757  7931  7931 I AndroidRuntime: Using default boot image
11-17 14:21:13.757  7931  7931 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:13.835  7931  7931 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:14.896  7931  7931 D AndroidRuntime: Shutting down VM
11-17 14:21:19.843  7954  7954 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:19.846  7954  7954 I AndroidRuntime: Using default boot image
11-17 14:21:19.846  7954  7954 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:19.924  7954  7954 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:20.996  7954  7954 D AndroidRuntime: Shutting down VM
11-17 14:21:25.945  7977  7977 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:25.949  7977  7977 I AndroidRuntime: Using default boot image
11-17 14:21:25.949  7977  7977 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:26.026  7977  7977 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:27.090  7977  7977 D AndroidRuntime: Shutting down VM
11-17 14:21:32.044  8003  8003 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:32.047  8003  8003 I AndroidRuntime: Using default boot image
11-17 14:21:32.047  8003  8003 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:32.124  8003  8003 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:33.183  8003  8003 D AndroidRuntime: Shutting down VM
11-17 14:21:38.112  8027  8027 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:38.115  8027  8027 I AndroidRuntime: Using default boot image
11-17 14:21:38.115  8027  8027 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:38.188  8027  8027 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:39.245  8027  8027 D AndroidRuntime: Shutting down VM
11-17 14:21:44.196  8050  8050 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:44.199  8050  8050 I AndroidRuntime: Using default boot image
11-17 14:21:44.199  8050  8050 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:44.272  8050  8050 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:45.337  8050  8050 D AndroidRuntime: Shutting down VM
11-17 14:21:50.276  8073  8073 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:50.279  8073  8073 I AndroidRuntime: Using default boot image
11-17 14:21:50.279  8073  8073 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:50.353  8073  8073 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:51.410  8073  8073 D AndroidRuntime: Shutting down VM
11-17 14:21:56.351  8111  8111 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
11-17 14:21:56.354  8111  8111 I AndroidRuntime: Using default boot image
11-17 14:21:56.354  8111  8111 I AndroidRuntime: Leaving lock profiling enabled
11-17 14:21:56.433  8111  8111 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
11-17 14:21:57.498  8111  8111 D AndroidRuntime: Shutting down VM


