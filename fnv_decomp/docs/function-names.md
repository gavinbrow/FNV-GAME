# Function names for the largest address-named functions

The build recipe (`build/units.json`), the link maps and the assembler key on the `FUN_<addr>` identifiers, so the live tree keeps them. This table is the rename map. `tools/apply_function_names.py <src-copy-dir>` rewrites a copy of `src/` (for the public export) with the new names; it never touches the build tree.

Sizes are bytes of the original function. Names come from referenced strings, named callees, enclosing class and file; functions with thin evidence were left alone.

| Address | Size | Old name | New name | Scope | Evidence |
|---|---|---|---|---|---|
| 0x00741500 | 26620 | `FUN_00741500` | `UpdateGame` | `CaravanGame` | CaravanGame member, 26 KB per-frame body; uses CGM_NPCTrackRect / CGM_PlayerTrackRect tiles (Caravan card game) |
| 0x00adf080 | 26108 | `FUN_00adf080` | `ProcessSoundMessage` | `fnv_00adf080::BSAudioManager_adf080` | BSAudioManager member taking SoundMessageRecord*; switches on GetType/GetArgument1/2 (audio message pump) |
| 0x0093e860 | 23042 | `FUN_0093e860` | `Update` | `TickPlayer` | TickPlayer member (float dt): per-frame player tick, UpdateTargetHealthHUD, physics-controller actor lookups |
| 0x00bebd20 | 18937 | `FUN_00bebd20` | `SetupShadowLightPasses` | `fnv_00bebd20` | shadowlightshader.cpp: builds beam stages, SetPixelShader/SetVertexShader/SetRenderState per pass |
| 0x00b74210 | 18282 | `FUN_00b74210` | `CompileShadowLightPixelShaders` | `ShaderCompiler` | ShaderCompiler member; formats SLS1%03i.pso / SLS2%03i.pso names, ps_2_0 profile |
| 0x00b4f9d0 | 17968 | `FUN_00b4f9d0` | `RegisterShaderTechniqueNames` | `Z::YAPBDH` | bsshadermanager.cpp: long table of BSSM_ZONLY/BSSM_CONSTALPHA... technique name strings via sprintf_s |
| 0x00428150 | 17170 | `FUN_00428150` | `LoadExtraData` | `ExtraDataLoader` | ExtraDataLoader member taking LoadBuffer*; reads per-type extra data records into the ExtraDataList |
| 0x0076bfe0 | 16523 | `FUN_0076bfe0` | `BuildHUDMainMenuTiles` | `YAPAVTile` | hudmainmenu: creates Tile* tree from template_meter, QuestStages, QuestAdded, Subtitles templates |
| 0x00ea7d40 | 14952 | `FUN_00ea7d40` | `SweptBoxBoxIntersect` | `YA_NMABUSweepBox` | niboxbv.cpp: SweepBox/SweepPoint SAT test with ClampPositionToBoxes |
| 0x00ea3d60 | 14124 | `FUN_00ea3d60` | `SweptBoxBoxIntersectRework` | `YA_NMABUReworkBox` | niboxbv.cpp: sibling of SweptBoxBoxIntersect using ReworkBox/ReworkPoint types |
| 0x00ce61c0 | 13246 | `FUN_00ce61c0` | `MapSkeletonPose` | `YAXABUHkMapperParams` | hkaskeletonmapperutils: HkMapperParams/HkMapperData, calls map_AtoB / map_BtoA |
| 0x004c37d0 | 12829 | `FUN_004c37d0` | `TransferItems` | `Transfer4c37C37This` | InventoryChanges transfer: leveled-item index, inventory slot extra data, Vcall into owner (many form/extra args) |
| 0x00ebc2a0 | 12792 | `FUN_00ebc2a0` | `FindIntersection` | `NiOBB` | NiOBB member: OBB-vs-OBB swept test using source velocity / delta time, IntersectRay |
| 0x00deab10 | 12441 | `FUN_00deab10` | `TestSeparatingAxes` | `YAHPBVhkVector4` | hkgeometryprocessing: isSeparatingAxis + calcEdgeAxis over two hkVector4 sets |
| 0x00734db0 | 12412 | `FUN_00734db0` | `UpdateMenu` | `BlackjackUpdate` | BlackjackUpdate member in blackjackmenu: UpdateBetTiles, DispatchMessageToSink |
| 0x0074fdc0 | 12012 | `FUN_0074fdc0` | `ChooseMove` | `CaravanOwner` | CaravanOwner member returning CaravanDecision; CanPlaceCard / UpdateHandStats (Caravan AI turn) |
| 0x00d6f460 | 11056 | `FUN_00d6f460` | `BuildJacobianFromAtoms` | `YAXPBUAtom` | hkpbuildjacobianfromatoms.cpp; switch over atom types (Atom*, QueryIn/QueryOut) |
| 0x00a04640 | 10120 | `FUN_00a04640` | `RenderTiles` | `RenderTile` | RenderTile member (tile_ob1_variant.cpp): RenderTextChanged, RenderResetTextures, lb_highlight_box |
| 0x00895110 | 10103 | `FUN_00895110` | `PickMovementAnimGroup` | `fnv_00895110::PickActor` | PickActor member (float,float): GetMoveAnimGroup, PickGroupType, GetBipedAnimation |
| 0x00d8fb70 | 9800 | `FUN_00d8fb70` | `StepConstraints` | `ConstraintStepImplementation` | hkpsolver: ConstraintStepImplementation over SolverSchemaHeader, stepJacobian |
| 0x00491180 | 9672 | `FUN_00491180` | `UpdateAnimationQueue` | `FUN_00491180_shell` | animation.cpp: HasQueuedSequences, AddAnimation, PlayGroupEx, QueueReloadGroup on a TESObjectREFR |
| 0x00888b50 | 9413 | `FUN_00888b50` | `UpdateActorFrame` | `ActorUpdateActor` | ActorUpdateActor member (float dt): Lock/ClearUpdate/GetProcess/Get3D/GetFaceGen, per-actor update |
| 0x006a37a0 | 9036 | `FUN_006a37a0` | `BuildNavMeshScene` | `NavRenderX` | NavRenderX member (CellX*, bool): GetNavMeshArray, AttachChildInAvailableSlot (navmesh debug render) |
| 0x0045dfe0 | 8357 | `FUN_0045dfe0` | `ClearAllFormLists` | `DataHandlerX` | TESDataHandler-style member: ClearItems/ClearField88 over every form list (data handler reset) |
| 0x005b1ba0 | 8348 | `FUN_005b1ba0` | `EncodeScriptParameter` | `YA_NGPBUEncodeParameter` | tesscriptcompiler: EncodeParameter/ScriptLineBuffer/EncodeCompiler, atol/atof/toupper parameter parsing |
| 0x00ab5ec0 | 8046 | `FUN_00ab5ec0` | `ReadFaceGenTri` | `fnv_00ab5ec0` | blk_00aa0000: FRTRI003 magic, reads material/shape/morph/partition byte blocks (FaceGen .tri) |
| 0x0073ea90 | 7732 | `FUN_0073ea90` | `LoadCaravanModels` | `fnv_0073ea90::CaravanMenuX` | CaravanMenuX member: formats Player_Deck.NIF, PlayerGrid_%i.NIF, OppGrid_%i.NIF, Select_Add.NIF |
| 0x004cbbc0 | 7678 | `FUN_004cbbc0` | `CleanInventory` | `InventoryClean` | InventoryClean member: CountAndPruneEntries, RemoveExtra24, SetWornState, GetArmorRating |
| 0x00eaff20 | 7673 | `FUN_00eaff20` | `RayTriangleSetSquaredDistance` | `YAMABVOriginDirectionPair` | nicollision: ray (OriginDirectionPair) vs TrianglePointSet squared distance, Cross/Dot/sqrtf |
| 0x0095a3b0 | 7402 | `FUN_0095a3b0` | `LoadPlayerGame` | `PlayerLoadState` | PlayerLoadState member (WkBuf*): ReadFormID, ReadRef, PlaceMarker, SortTopicList (PlayerCharacter::LoadGame) |
| 0x00ab7f40 | 7294 | `FUN_00ab7f40` | `WriteFaceGenTri` | `TriWriterRework::YA_NPAUWriter` | TriWriterRework Writer: writes the counterpart FaceGen .tri data with ReportError / bufferA |
| 0x00e1f4e0 | 7195 | `FUN_00e1f4e0` | `FillHoles` | `FillHolesMesh` | hkgpmesh FillHolesMesh member: LocatePoint, scanFlip, CheckLinks (mesh hole filling) |
| 0x0089d900 | 7128 | `FUN_0089d900` | `Kill` | `KillActor` | KillActor member (Actor*, float): KillSupport::ApplyHavokOperation, IncrementCount (actor death) |
| 0x004ce380 | 6805 | `FUN_004ce380` | `MoveItems` | `InventoryMove` | InventoryMove member: MoveItem, IsQuestItem, DispatchMessageToSink with %i %s%s %s message formats |
| 0x009445b0 | 6764 | `FUN_009445b0` | `UpdateAimAndScope` | `AimPlayer` | AimPlayer member: ClampLookAngle, SetYaw, UpdateScopeZoom, ProjectToScreen |
| 0x007bd2a0 | 6752 | `FUN_007bd2a0` | `UpdateMenu` | `fnv_007bd2a0::RouletteMenuX` | RouletteMenuX member: GAMERouletteValidBet, UpdateBetTileText, RotateRouletteWheelToResult |
| 0x00523150 | 6505 | `FUN_00523150` | `Fire` | `FireWeapon` | FireWeapon member (FireRef*): GetCurrentAmmo, ApplyPerkModifiers, GetWeaponType (Weapon fire) |
| 0x00955620 | 6476 | `FUN_00955620` | `SavePlayerGame` | `PlayerSave` | PlayerSave member (uint): SaveLog, SaveGame, ForwardToSaveLoadGame (PlayerCharacter::SaveGame) |
| 0x00b55bb0 | 6253 | `FUN_00b55bb0` | `CreateDefaultTextures` | `YAXXZ` | bsshadermanager_nogf_variant.cpp: BSShader_DefErrorMap/DefNormalMap/DefHeightMap... generated procedurally |
| 0x00db2960 | 6169 | `FUN_00db2960` | `CalculateManifold` | `Manifold::NDetector` | hkpboxboxcollisiondetection NDetector const member filling Manifold with AddContactPoint |
| 0x00cdbae0 | 6120 | `FUN_00cdbae0` | `SolveTwoJointIK` | free function | strings LtTWOJOINTSOLVER, StINIT, StFIXLENGTH, StFIXDIRECTION; hinge/target rotation math |
| 0x0078eb50 | 5952 | `FUN_0078eb50` | `UpdateMenu` | `fnv_0078eb50::xLockPickMenu` | xLockPickMenu member in lockpickmenu.cpp: per-frame input (GetAxisState) and audio |
| 0x00df37b0 | 5898 | `FUN_00df37b0` | `BuildSubtree` | `hkKdTreeBuilder` | hkKdTreeBuilder static member: recursive build over WorkingSet / KdTreeNode |
| 0x008e0f80 | 5887 | `FUN_008e0f80` | `UpdateFollow` | `fnv_008e0f80::FollowProcess` | FollowProcess member: SetFollowing/ClearFollowing, FindTarget, IsBlocked, StopMoving |
| 0x00c56680 | 5863 | `FUN_00c56680` | `BuildSphereMesh` | `SphereBuild::YAPAUFUN_00a5ecb0` | SphereBuild: SphereCos/SphereSin tables, Vec3/Vec2 vertex fill, returns mesh node |
| 0x00dd3210 | 5720 | `FUN_00dd3210` | `queryRayBundle` | `RayBundleTraversalMachine` | hkpMoppRayBundleVirtualMachine: RayBundleTraversalMachine over QueryState / RayQuerySet |
| 0x00b827c0 | 5647 | `FUN_00b827c0` | `LoadWaterShaders` | `WaterShaderLoader` | WaterShaderLoader member: WATER000.vso/WATER001.vso/WATER002.vso, vs_1_1/ps_2_0/ps_3_0 compile |
| 0x00707e30 | 5622 | `FUN_00707e30` | `FillItemDisplayTile` | `YAXPAUDisplayItem` | interface.cpp (DisplayItem*, DisplayTile*): weapon damage/ammo/effect text via BuildDescription |
| 0x005accb0 | 5564 | `FUN_005accb0` | `ExtractScriptArguments` | `YA_NPBUExtractParameter` | tesscript.cpp variadic va_arg extractor: ExtractParameter table, ReadScriptValue, form lookup |
| 0x00ea0ad0 | 5462 | `FUN_00ea0ad0` | `SqrDistSegmentBox` | `YA_NMABVOBoxBV` | nicollision OBoxBV: SqrDistSegBox / SqrDistPtBox helper chain |
| 0x0077c4e0 | 5454 | `FUN_0077c4e0` | `UpdateXPDisplay` | `XPMenu` | XPMenu member: LookupXPTrait, PendingLevels, strings _x_max, UILevelUpText |
| 0x00bb4740 | 5446 | `FUN_00bb4740` | `BuildParticleShaderPasses` | `P368Shader` | P368Shader member: IsParticleShaderRendererEnabled, SortShadowSceneLights, AllocateElemArray |
| 0x0094ae40 | 5433 | `FUN_0094ae40` | `UpdatePlayerCameraState` | `fnv_0094ae40::Obj117` | Obj117 member in playercharacter: UpdateCameraShake, SetLookAt, GetMinBlendValue |
| 0x00d24b50 | 5414 | `FUN_00d24b50` | `castRay` | `SampledHeightRayCastView` | SampledHeightRayCastView: hkpSampledHeightFieldShape ray cast (string rcHeightFild) |
| 0x00eb1d20 | 5385 | `FUN_00eb1d20` | `RayTriangleSquaredDistance` | `fnv_00eb1d20` | same family; single Triangle3D, GetSquaredDistanceToTriangle |
| 0x0056b2d0 | 5250 | `FUN_0056b2d0` | `Load3D` | `BuildReferenceScene::Reference` | Reference member of BuildReferenceScene in tesobjectrefr.cpp: builds scene node, RandomPhase, update slots |
| 0x009466d0 | 5175 | `FUN_009466d0` | `ProcessInput` | `InputPlayer` | InputPlayer member (float, bool): GetAxisState, speed/Query22C input handling |
| 0x00796fd0 | 5100 | `FUN_00796fd0` | `HandleClick` | `MapMenuClick` | MapMenuClick member (int, Tile*): SelectNote, UpdateSelectedQuestMarkers, UIPopUpMapMarkerAdded |
| 0x00834260 | 5097 | `FUN_00834260` | `UpdateRadioStation` | `FalloutRadio::YAXPAVRadioStationState` | falloutradio.cpp (RadioStationState*): PlayAudioMedia, AdvanceConversation, thread flags |
| 0x00607990 | 5090 | `FUN_00607990` | `ActivateNPC` | `TESNPCActivate` | TESNPCActivate member: GetIsDying, GetCurrentTalkTarget, IsGuard, knock state checks |
| 0x009c7240 | 5052 | `FUN_009c7240` | `UpdateDialogueCamera` | `DialogueCameraX` | DialogueCameraX member: xSetDialogueActive, StartTopic, GetCamData |
| 0x00779070 | 5007 | `FUN_00779070` | `UpdateCompassTiles` | `fnv_00779070` | hudmainmenu.cpp (CompassMovie*, CompassTileList*): GetAngleZ, GetMapMarkers, UIPopUpQuestNew |
| 0x00e4c730 | 4956 | `FUN_00e4c730` | `getClosestPoint` | `Gsk` | Gsk member returning GskStatus: GetSupportPoint, GetVerticesForIds (hkGsk) |
| 0x004235e0 | 4950 | `FUN_004235e0` | `SaveExtraDataList` | `extra_save::SaveShell` | SaveShell (extra_save) member: WriteScriptLocals, vf save calls (extradatalist save path) |
| 0x00b19ad0 | 4804 | `FUN_00b19ad0` | `BuildFrond` | `FrondBuilder` | FrondBuilder member (FrondInput*), speedtree frondengine: FrondPoint, ScaleSwizzled |
| 0x009590f0 | 4786 | `FUN_009590f0` | `SaveToBuffer` | `PlayerX` | PlayerX member (BufferX*): SaveData, SaveFormData, SaveAnimData, SerializeFormData |
| 0x007ddf00 | 4625 | `FUN_007ddf00` | `UpdateActiveEffects` | `StatsMenuActiveEffects` | StatsMenuActiveEffects member: stats_rad_effect_/h20/sleep templates, radiation/dehydration stages |
| 0x00815d00 | 4611 | `FUN_00815d00` | `FindTargets` | `CastTargets::Caster` | CastTargets::Caster member: GatherTargetsInArea, GetReach, FindCostliestEffectItem |
| 0x005aff40 | 4568 | `FUN_005aff40` | `CompileBlockLines` | `LineCompiler` | LineCompiler member (CompileScript*, CompileState*, CompileLine*): CompileScriptLine, ConvertToPostfix |
| 0x00a12fb0 | 4544 | `FUN_00a12fb0` | `LayoutTextString` | `TextLayout::Font` | TextLayout::Font member (const char*, Layout*): AllocateText, NormalizeSmartQuotes, icon lookup |
| 0x00634e20 | 4538 | `FUN_00634e20` | `InitializeMoon` | `MoonInit` | MoonInit member (NiNode*, const char*): builds moon NiTriShape, SkyObject::Initialize |
| 0x00bba5d0 | 4534 | `FUN_00bba5d0` | `LoadPixelShaders` | `SM3ShaderLoader` | SM3ShaderLoader member: SPECULAR/HAIR/PARALLAX/PARALLAXOCC/FACEGENBLEND macros, CreatePixelShader |
| 0x0086a850 | 4532 | `FUN_0086a850` | `WinMain` | `Z::YGHIIII` | main.cpp __stdcall (4 uints): CreateMutexA single-instance guard, FindWindow, CommandLineToArgvW, ShellExecute |
| 0x00baafc0 | 4502 | `FUN_00baafc0` | `InitPrograms` | `TallGrassPrograms` | TallGrassPrograms member: emits vertex[n].macros[...] tables via FindGrassMacroEnd |
| 0x005f3a20 | 4432 | `FUN_005f3a20` | `CreateAnimGroupFromSequence` | `fnv_005f3a20` | tesanimgroup.cpp: NiControllerSequenceEx + filename, ParseAnimationGroupFilename, text keys |
| 0x00770430 | 4332 | `FUN_00770430` | `UpdateHUD` | `HUDUpdate` | HUDUpdate member of hudmainmenu: UpdateAmmoHUD, UpdateCompassMarkers, UpdateRadMeter, UpdateQuestNotification |
| 0x00bdf790 | 4317 | `FUN_00bdf790` | `AddRenderPasses` | `fnv_00bdf790::PShader` | PShader member: AddRenderPass, AddShadowPass, SelectTwoLightPass, AddAdditionalPass |
| 0x00610cd0 | 4310 | `FUN_00610cd0` | `Load` | `RaceLoadDetail::RaceLoadTarget` | RaceLoadTarget member (TESFile*): LoadRecordHeader, ReadFullName, SetDefaultVoiceType (TESRace::Load) |
| 0x00602190 | 4172 | `FUN_00602190` | `LoadNPCRecord` | `NpcLoadShell` | NpcLoadShell member (TESFile*): calls TESNPC::Load pieces, readOBNDSubRecord, SetEditorID_AtRuntime |
| 0x00ab46f0 | 4131 | `FUN_00ab46f0` | `CopyFrom` | `CopyCollection` | CopyCollection member (const CopyCollection*): Resize_coordinates/normals/colors/tangents then Copy32 |
| 0x00640810 | 4121 | `FUN_00640810` | `InitializeSun` | `fnv_00640810::FUN_00640810_t` | FUN_00640810_t (sky/sun.cpp): builds sun NiTriShape, SetEffectColor, AddProperties |
| 0x009ff970 | 4043 | `FUN_009ff970` | `RegisterTileTraits` | `TraitRegistration` | tile.cpp TraitRegistration: registers trait types/depths for Tile (SetDepth, GetType) |
| 0x00c95a80 | 4000 | `FUN_00c95a80` | `Construct` | `WorldCtor` | WorldCtor member (WorldInfoCtor*, int): hkpWorld constructor, strings about code built with [..] |
| 0x00534ad0 | 3981 | `FUN_00534ad0` | `Load` | `TESLandL53` | TESLandL53 member (TESFileL53*): ReadData, IsBigEndian swap, chunk ids (TESLand::Load) |
| 0x00530160 | 3907 | `FUN_00530160` | `CopyFrom` | `TESImageSpaceModifierCopy` | TESImageSpaceModifierCopy member (TESForm*): CacheObjectValues, BlendColor/BlendPoint copy |
| 0x007da2c0 | 3837 | `FUN_007da2c0` | `BuildStatsMenuTiles` | `YAPAVTile` | statsmenu.cpp Tile* factory: stats_list_template, stats_effects_template, _rads/_h20/_sleep |
| 0x00dd1f30 | 3761 | `FUN_00dd1f30` | `queryLongRay` | `LongRayTreeDetail::MoppMachine` | MoppMachine::LongRayTreeDetail member: ray query over RayState/RayPair |
| 0x00d1a330 | 3729 | `FUN_00d1a330` | `computeEntityAabbs` | free function | hkpentityaabbutil: getAabb, getSweptTransform, getShape over child shape keys |
| 0x0086d590 | 3667 | `FUN_0086d590` | `InitializeRenderSystem` | `fnv_0086d590::RenderSystem` | RenderSystem member in main.cpp: scene graph, BSFogProperty, SetDepthParams (render system setup) |
| 0x00cb6060 | 3600 | `FUN_00cb6060` | `SplitSimulationIsland` | `YAXPAUSplitIsland_Arg0` | hkpworld util: SplitIsland_* helpers (classifyParts, combineGroups, CheckConnectivity) |
| 0x00d28a30 | 3580 | `FUN_00d28a30` | `stepMotions` | free function | hkprigidmotionutil: integrateMotion, applyGravity, applyDamping, clampVelocities |
| 0x004dd2c0 | 3504 | `FUN_004dd2c0` | `QueryEyefinityDisplays` | `YAHHPAUEFEyefinityInfo` | blk_004c0000: LoadLibrary atiadlxx.dll, ADL_Adapter_NumberOfAdapters_Get / ADL_Display_Modes_Get |
| 0x00aeb270 | 3447 | `FUN_00aeb270` | `OpenStream` | `xGameSound` | xGameSound member: TryStream, .mp3/.ogg extension probing, mmioOpen/Descend |
| 0x004d66d0 | 3432 | `FUN_004d66d0` | `PopulateObjectViewer` | `fnv_004d66d0::ObjectTree` | ObjectTree member: Scale %.1f, Culled, Attributes, Properties strings (scene-graph viewer text) |
| 0x00e4f910 | 3389 | `FUN_00e4f910` | `runTransformTrackAnalysis` | `YAXPAUTrackBuffers_e50650` | hkatrackanalysis: single call to analyzeTransformTracks with TrackBuffers |
| 0x00bcd7c0 | 3389 | `FUN_00bcd7c0` | `LoadPixelShaders` | `PixelLoader` | PixelLoader member: emits desc[n].macros[...] tables for pixel shader descriptors |
| 0x005f7ec0 | 3300 | `FUN_005f7ec0` | `Load` | `CreatureRecord` | CreatureRecord member (CreatureRecordFile*): LoadBounds, ReadFullName, ReadChunkInt (TESCreature::Load) |
| 0x00b2ed70 | 3258 | `FUN_00b2ed70` | `JoinStrips` | `StripJoin::Mesh` | speedtree StripJoin::Mesh member: newStrips/newLengths/newCounts rebuilt into joined strips |
| 0x007c40b0 | 3253 | `FUN_007c40b0` | `SetReelTextures` | `ReelMenu` | ReelMenu member in slotmachinemenu.cpp: SetTexture per reel symbol |
| 0x00adddd0 | 3252 | `FUN_00adddd0` | `UpdateAudioSystem` | `fnv_00adddd0::AudioUpdate` | AudioUpdate member in bsaudiomanager: GetTickCount, AddSound, message queue push |
| 0x00997cf0 | 3216 | `FUN_00997cf0` | `UpdateCombatState` | `fnv_00997cf0::CombatUpdate` | CombatUpdate member in combatstate.cpp: UpdateTargetPerception, FindNearestActor |
| 0x00d302d0 | 3185 | `FUN_00d302d0` | `processCollision` | `BvTreeAgentD3` | BvTreeAgentD3 member: strings LtBvTree/StQueryTree/StNarrowPhase (hkpBvTreeAgent) |
| 0x00ae5ff0 | 3070 | `FUN_00ae5ff0` | `BuildDebugList` | `AudioSystem` | AudioSystem member (uint) returning DebugList*: enumerates sounds under critical section, strcat/sprintf |
